import json
from glob import glob
import datetime
import hashlib
import logging
import traceback

import iatikit
import sqlalchemy as sa
from dateutil.parser import parse as date_parser
from flask import Blueprint
import click

from iatilib import db, parse, rq
from iatilib.model import Dataset, Resource, Activity, Log, DeletedActivity
from iatilib.loghandlers import DatasetMessage as _

log = logging.getLogger("crawler")


manager = Blueprint('crawler', __name__)
manager.cli.short_help = "Crawl IATI registry"


def fetch_dataset_list(modified_since=None):
    '''
    Fetches datasets from CKAN and stores them in the DB. Either passed a datetime to filter on more recently modified
    datasets, or updates the entire set. Used in update() to update the Flask job queue. Uses CKAN metadata to determine
    if an activity is active or deleted, and tries to determine if a dataset is actually new or not.
    :param modified_since:
    :return:
    '''
    existing_datasets = Dataset.query.all()
    existing_ds_names = set((ds.publisher, ds.name) for ds in existing_datasets)

    if modified_since and iatikit.data()._last_updated > modified_since:
        return Dataset.query.filter(sa.sql.false())

    iatikit.download.data()

    package_list = [
        tuple(x[:-4].rsplit('/', 2)[1:])
        for x in glob('__iatikitcache__/registry/data/*/*')]
    incoming_ds_names = set(package_list)

    new_datasets = [Dataset(name=n, publisher=p) for p, n
                    in incoming_ds_names - existing_ds_names]
    all_datasets = existing_datasets + new_datasets
    for dataset in all_datasets:
        dataset.last_seen = datetime.datetime.utcnow()

    db.session.add_all(all_datasets)
    db.session.commit()

    deleted_ds_names = existing_ds_names - incoming_ds_names
    if deleted_ds_names:
        delete_datasets([d[1] for d in deleted_ds_names])

    all_datasets = Dataset.query
    return all_datasets


def delete_datasets(datasets):
    deleted_datasets = db.session.query(Dataset).filter(Dataset.name.in_(datasets))

    activities_to_delete = db.session.query(Activity). \
        filter(Activity.resource_url == Resource.url). \
        filter(Resource.dataset_id.in_(datasets))

    now = datetime.datetime.now()
    deleted_activities = [DeletedActivity(
            iati_identifier=a.iati_identifier,
            deletion_date=now
    )
                          for a in activities_to_delete]
    db.session.add_all(deleted_activities)
    db.session.commit()
    deleted = deleted_datasets.delete(synchronize_session='fetch')
    log.info("Deleted {0} datasets".format(deleted))
    return deleted


def fetch_dataset_metadata(dataset):
    fname = '__iatikitcache__/registry/metadata/{0}/{1}.json'.format(
        dataset.publisher, dataset.name)
    with open(fname) as f:
        ds_entity = json.load(f)

    dataset.last_modified = date_parser(
        ds_entity.get(
            'metadata_modified',
            datetime.datetime.now().date().isoformat()))
    new_urls = [resource['url'] for resource
                in ds_entity.get('resources', [])
                if resource['url'] not in dataset.resource_urls]
    dataset.resource_urls.extend(new_urls)

    urls = [resource['url'] for resource
            in ds_entity.get('resources', [])]
    for deleted in set(dataset.resource_urls) - set(urls):
        dataset.resource_urls.remove(deleted)

    try:
        dataset.license = ds_entity['license']
    except KeyError:
        pass
    dataset.is_open = ds_entity.get('isopen', False)
    db.session.add(dataset)
    try:
        db.session.commit()
    except sa.exc.IntegrityError:
        db.session.rollback()
    return dataset


def fetch_resource(resource):
    '''
    Gets the resource using the request library and sets the times of last successful update based on the status code.
    :param resource:
    :return:
    '''
    dataset = Dataset.query.get(resource.dataset_id)
    fname = '__iatikitcache__/registry/data/{0}/{1}.xml'.format(
        dataset.publisher, dataset.name)
    with open(fname, 'rb') as f:
        content = f.read()

    resource.document = content
    resource.last_succ = datetime.datetime.utcnow()
    resource.last_parsed = None
    resource.last_parse_error = None

    db.session.add(resource)
    return resource


def check_for_duplicates(activities):
    if activities:
        dup_activity = Activity.query.filter(
                Activity.iati_identifier.in_(
                        a.iati_identifier for a in activities
                )
        )
        with db.session.no_autoflush:
            for db_activity in dup_activity:
                res_activity = next(
                        a for a in activities
                        if a.iati_identifier == db_activity.iati_identifier
                )
                activities.remove(res_activity)
                db.session.expunge(res_activity)
    return activities


def hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.digest()


def parse_activity(new_identifiers, old_xml, resource):
    for activity in parse.document(resource.document, resource):
        activity.resource = resource

        if activity.iati_identifier not in new_identifiers:
            new_identifiers.add(activity.iati_identifier)
            try:
                if hash(activity.raw_xml) == old_xml[activity.iati_identifier][1]:
                    activity.last_change_datetime = old_xml[activity.iati_identifier][0]
                else:
                    activity.last_change_datetime = datetime.datetime.now()
            except KeyError:
                activity.last_change_datetime = datetime.datetime.now()
            db.session.add(activity)
            check_for_duplicates([activity])
        else:
            parse.log.warn(
                    _("Duplicate identifier {0} in same resource document".format(
                            activity.iati_identifier),
                      logger='activity_importer', dataset=resource.dataset_id, resource=resource.url),
                    exc_info=''
            )

        db.session.flush()
    db.session.commit()


def parse_resource(resource):
    db.session.add(resource)
    now = datetime.datetime.utcnow()
    current = Activity.query.filter_by(resource_url=resource.url)
    current_identifiers = set([i.iati_identifier for i in current.all()])

    # obtains the iati-identifier, last-updated datetime, and a hash of the existing xml associated with
    # every activity associated with the current url.
    old_xml = dict([(i[0], (i[1], hash(i[2]))) for i in db.session.query(
            Activity.iati_identifier, Activity.last_change_datetime,
            Activity.raw_xml).filter_by(resource_url=resource.url)])

    db.session.query(Activity).filter_by(resource_url=resource.url).delete()
    new_identifiers = set()
    parse_activity(new_identifiers, old_xml, resource)

    resource.version = parse.document_metadata(resource.document)

    # add any identifiers that are no longer present to deleted_activity table
    diff = current_identifiers - new_identifiers
    now = datetime.datetime.utcnow()
    deleted = [
        DeletedActivity(iati_identifier=deleted_activity, deletion_date=now)
        for deleted_activity in diff]
    if deleted:
        db.session.add_all(deleted)

    # remove any new identifiers from the deleted_activity table
    if new_identifiers:
        db.session.query(DeletedActivity) \
            .filter(DeletedActivity.iati_identifier.in_(new_identifiers)) \
            .delete(synchronize_session="fetch")

    log.info(
            "Parsed %d activities from %s",
            resource.activities.count(),
            resource.url)
    resource.last_parsed = now
    return resource  # , new_identifiers


def update_activities(dataset_name):
    '''
    Parses and stores the raw XML associated with a resource [see parse_resource()], or logs the invalid resource
    :param resource_url:
    :return:
    '''
    # clear up previous job queue log errors
    db.session.query(Log).filter(sa.and_(
            Log.logger == 'job iatilib.crawler.update_activities',
            Log.resource == dataset_name,
    )).delete(synchronize_session=False)
    db.session.commit()

    dataset = Dataset.query.get(dataset_name)
    resource = dataset.resources[0]
    try:
        db.session.query(Log).filter(sa.and_(
                Log.logger.in_(
                        ['activity_importer', 'failed_activity', 'xml_parser']),
                Log.resource == dataset_name,
        )).delete(synchronize_session=False)
        parse_resource(resource)
        db.session.commit()
    except parse.ParserError as exc:
        db.session.rollback()
        resource.last_parse_error = str(exc)
        db.session.add(Log(
                dataset=resource.dataset_id,
                resource=resource.url,
                logger="xml_parser",
                msg="Failed to parse XML file {0} error was".format(dataset_name, exc),
                level="error",
                trace=traceback.format_exc(),
                created_at=datetime.datetime.now()
        ))
        db.session.commit()


def update_dataset(dataset_name):
    '''
    Takes the dataset name and determines whether or not an update is needed based on whether or not the last
    successful update detail exits, and whether or not it last updated since the contained data was updated.
    :param dataset_name:
    :return:
    '''
    # clear up previous job queue log errors
    db.session.query(Log).filter(sa.and_(
            Log.logger == 'job iatilib.crawler.update_dataset',
            Log.dataset == dataset_name,
    )).delete(synchronize_session=False)
    db.session.commit()

    queue = rq.get_queue()
    dataset = Dataset.query.get(dataset_name)

    fetch_dataset_metadata(dataset)
    fetch_resource(dataset.resources[0])
    db.session.commit()

    queue.enqueue(update_activities, args=(dataset_name,), result_ttl=0, timeout=100000)


@manager.cli.command('dataset_list')
def dataset_list():
    fetch_dataset_list()
    db.session.commit()


@manager.cli.command('metadata')
def metadata(verbose=False):
    for dataset in Dataset.query.all():
        if verbose:
            print("Fetching metadata for %s" % dataset.name)
        fetch_dataset_metadata(dataset)


@manager.cli.command('documents')
def documents(verbose=False):
    for dataset in Dataset.query.all():
        if verbose:
            print("Fetching documents for %s" % dataset.name)
        for resource in dataset.resources:
            if verbose:
                print("Fetching %s" % resource.url,)
            try:
                fetch_resource(resource)
            except IOError:
                print("Failed to fetch %s" % resource.url,)
            db.session.commit()


def status_line(msg, filt, tot):
    total_count = tot.count()
    filtered_count = filt.count()
    try:
        ratio = 1.0 * filtered_count / total_count
    except ZeroDivisionError:
        ratio = 0.0
    return "{filt_c:4d}/{tot_c:4d} ({pct:6.2%}) {msg}".format(
            filt_c=filtered_count,
            tot_c=total_count,
            pct=ratio,
            msg=msg
    )


@click.option('--dataset', 'dataset', type=str)
@manager.cli.command('manual_update')
def manual_update(dataset=None):
    """Update a single dataset"""
    if dataset:
        print("Updating {0}".format(dataset))
        ds = Dataset.query.get(dataset)
        fetch_dataset_metadata(ds)
        db.session.commit()
        res = Resource.query.filter(Resource.dataset_id == dataset)
        for resource in res:
            fetch_resource(resource)
            db.session.commit()
            update_activities(resource.url)


@manager.cli.command('status')
def status():
    """Show status of current jobs"""
    print("%d jobs on queue" % rq.get_queue().count)

    print(status_line(
            "datasets have no metadata",
            Dataset.query.filter_by(last_modified=None),
            Dataset.query,
    ))

    print(status_line(
            "datasets not seen in the last day",
            Dataset.query.filter(Dataset.last_seen <
                                 (datetime.datetime.utcnow() - datetime.timedelta(days=1))),
            Dataset.query,
    ))

    print(status_line(
            "resources have had no attempt to fetch",
            Resource.query.outerjoin(Dataset).filter(
                    Resource.last_fetch == None),
            Resource.query,
    ))

    print(status_line(
            "resources not successfully fetched",
            Resource.query.outerjoin(Dataset).filter(
                    Resource.last_succ == None),
            Resource.query,
    ))

    print(status_line(
            "resources not fetched since modification",
            Resource.query.outerjoin(Dataset).filter(
                    sa.or_(
                            Resource.last_succ == None,
                            Resource.last_succ < Dataset.last_modified)),
            Resource.query,
    ))

    print(status_line(
            "resources not parsed since mod",
            Resource.query.outerjoin(Dataset).filter(
                    sa.or_(
                            Resource.last_succ == None,
                            Resource.last_parsed < Dataset.last_modified)),
            Resource.query,
    ))

    print(status_line(
          "resources have no activites",
          db.session.query(Resource.url).outerjoin(Activity)
          .group_by(Resource.url)
          .having(sa.func.count(Activity.iati_identifier) == 0),
          Resource.query))

    print("")

    total_activities = Activity.query.count()
    # out of date activitiy was created < resource last_parsed
    total_activities_fetched = Activity.query.join(Resource).filter(
        Activity.created < Resource.last_parsed).count()
    try:
        ratio = 1.0 * total_activities_fetched / total_activities
    except ZeroDivisionError:
        ratio = 0.0
    print("{nofetched_c}/{res_c} ({pct:6.2%}) activities out of date".format(
            nofetched_c=total_activities_fetched,
            res_c=total_activities,
            pct=ratio
    ))


@manager.cli.command('enqueue')
def enqueue(careful=False):
    queue = rq.get_queue()
    if careful and queue.count > 0:
        print("%d jobs on queue, not adding more" % queue.count)
        return

    yesterday = datetime.datetime.utcnow() - datetime.timedelta(days=1)

    unfetched_resources = Resource.query.filter(
            sa.or_(
                    Resource.last_fetch == None,
                    sa.and_(
                            Resource.last_succ == None,
                            Resource.last_fetch <= yesterday
                    )))
    print("Enqueuing {0:d} unfetched resources".format(
            unfetched_resources.count()
    ))
    for resource in unfetched_resources:
        queue.enqueue(
                update_resource,
                args=(resource.url,),
                result_ttl=0)

    ood_resources = Resource.query.filter(sa.or_(
            Resource.last_parsed == None,
            Resource.activities.any(Activity.created < Resource.last_parsed)
    ))

    print("Enqueuing {0:d} resources with out of date activities".format(
            ood_resources.count()
    ))
    for resource in ood_resources:
        queue.enqueue(
                update_activities,
                args=(resource.url,),
                result_ttl=0,
                timeout=100000)


@click.option('--dataset', 'dataset', type=str,
              help="update a single dataset")
@click.option('--limit', "limit", type=int,
              help="max no of datasets to update")
@click.option('-v', '--verbose', "verbose")
@click.option('-t', '--timedelta', "timedelta", type=int)
@manager.cli.command('update')
def update(verbose=False, limit=None, dataset=None, timedelta=None):
    """
    Fetch all datasets from IATI registry; update any that have changed.
    This is done by adding to the dataset table, and then adding an update command to
    the Flask job queue. See fetch_dataset_list, then update_dataset for next actions.
    """
    queue = rq.get_queue()

    if dataset:
        print("Enqueuing {0} for update".format(dataset))
        queue.enqueue(update_dataset, args=(dataset,), result_ttl=0)
    else:
        if timedelta:
            modified_since = datetime.datetime.now() - datetime.timedelta(timedelta)
        else:
            modified_since = None
        datasets = fetch_dataset_list(modified_since)
        db.session.commit()

        if limit:
            datasets = datasets.limit(limit)

        print("Enqueuing %d datasets for update" % datasets.count())

        for dataset in datasets:
            if verbose:
                print("Enqueuing %s" % dataset.name)
            queue.enqueue(update_dataset, args=(dataset.name,), result_ttl=0)
    db.session.close()
