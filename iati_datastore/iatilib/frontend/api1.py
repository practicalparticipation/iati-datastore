from collections import namedtuple, OrderedDict
from datetime import datetime
import sqlalchemy as sa
from flask import (current_app, request, Response, Blueprint,
                   jsonify, abort, render_template, make_response,
                   url_for)
from flask.views import MethodView
from werkzeug.datastructures import MultiDict

from iatilib import db
from iatilib.model import (Resource, Dataset,
                           Log, DeletedActivity, Stats)

from . import dsfilter, validators, serialize


api = Blueprint('api1', __name__)
Scrollination = namedtuple('Scrollination', 'query offset limit total items')


@api.route('/')
def list_routes():
    urls = []
    rules = [
        r for r in current_app.url_map.iter_rules()
        if r.endpoint.startswith('api1.')]
    for rule in rules:
        options = {
            arg: arg.upper()
            for arg in rule.arguments
            if arg not in rule.defaults
        }
        url = url_for(rule.endpoint, _external=True, **options)
        urls.append(url)
    urls = sorted(urls)
    return jsonify(urls)


@api.route('/meta/filters/')
def meta_filters():
    return jsonify({
        'filters': list(validators.activity_api_args.schema.keys())
        })


@api.route('/about/')
def about():
    # General status info
    count_activities = db.session.query(
        Stats.count
    ).filter_by(label='activities').scalar()

    count_transactions = db.session.query(
        Stats.count
    ).filter_by(label='transactions').scalar()

    count_budgets = db.session.query(
        Stats.count
    ).filter_by(label='budgets').scalar()

    # Check last updated times

    updated = db.session.query(
        sa.func.max(Resource.last_fetch).label('last_fetch'),
        sa.func.max(Resource.last_succ).label('last_succ'),
        sa.func.max(Resource.last_parsed).label('last_parsed')
    ).first()
    now = datetime.now()
    # If the file was last fetched less than 2 days
    # ago and parsed less than 1 day
    # ago, then the API is healthy.
    if ((updated.last_fetch is not None) and
            (updated.last_succ is not None) and
            (updated.last_parsed is not None)):
        healthy = (
            ((now-updated.last_fetch).days < 2) and
            ((now-updated.last_succ).days < 2) and
            ((now-updated.last_parsed).days < 1)
        )
    else:
        healthy = False
    return jsonify(
        ok=healthy,
        status={True: 'healthy', False: 'unhealthy'}[healthy],
        status_data={
            'last_fetch': updated.last_fetch,
            'last_successful_fetch': updated.last_succ,
            'last_parsed': updated.last_parsed
        },
        indexed_activities=count_activities,
        indexed_transactions=count_transactions,
        indexed_budgets=count_budgets,
    )


@api.route('/about/dataset/')
def datasets():
    datasets = db.session.query(Dataset.name)
    return jsonify(datasets=[i.name for i in datasets.all()])


@api.route('/about/dataset/<dataset>/')
def about_dataset(dataset):
    dataset = db.session.query(Dataset).get(dataset)
    if dataset is None:
        abort(404)
    resources = []
    for r in dataset.resources:
        resources.append({
            'url': r.url,
            'last_fetch': r.last_fetch.isoformat() if r.last_fetch else None,
            'last_status_code': r.last_status_code,
            'last_successful_fetch': r.last_succ.isoformat() if r.last_succ else None,
            'last_parsed': r.last_parsed.isoformat() if r.last_parsed else None,
            'num_of_activities': r.activities.count(),
        })

    return jsonify(
            dataset=dataset.name,
            last_modified=None if dataset.last_modified is None else dataset.last_modified.isoformat(),
            num_resources=len(dataset.resources),
            resources=resources,
    )


@api.route('/about/datasets/fetch_status/')
def fetch_status_about_dataset():
    """Output a JSON formatted list of dataset dictionaries containing their resource details.

    Warning:
        This is an experimental API call and not intended for general use.

    """
    dataset_resources = db.session.query(Dataset).options(db.subqueryload(Dataset.resources))
    datasets = dict()

    for dataset in dataset_resources:
        if len(dataset.resources) == 0:
            continue
        ds_r = dataset.resources[0]
        resources = {
            'url': ds_r.url,
            'last_fetch': ds_r.last_fetch.isoformat() if ds_r.last_fetch else None,
            'last_status_code': ds_r.last_status_code,
            'last_successful_fetch': ds_r.last_succ.isoformat() if ds_r.last_succ else None,
            'last_parsed': ds_r.last_parsed.isoformat() if ds_r.last_parsed else None,
        }
        datasets[dataset.name] = resources

    return jsonify(datasets=[{dataset: datasets[dataset]} for dataset in datasets])


@api.route('/about/deleted/')
def deleted_activities():
    try:
        valid_args = validators.pagination_args(MultiDict(request.args))
    except (validators.MultipleInvalid, validators.Invalid) as e:
        return make_response(
            render_template('error/invalid_filter.html', errors=e), 400)
    offset = valid_args.get("offset", 0)
    limit = valid_args.get("limit", 50)
    query = db.session.query(
        DeletedActivity)\
        .order_by(DeletedActivity.deletion_date.desc())\
        .limit(limit).offset(offset)

    items = [
        {
            'iati_identifier': da.iati_identifier,
            'deletion_date': da.deletion_date.isoformat(),
        }
        for da in query
    ]

    return jsonify(OrderedDict((
            ("ok", True),
            ("total-count", query.count()),
            ("start", offset),
            ("limit", limit),
            ("deleted_activities", items),
        )
    ))


@api.route('/error/dataset/')
def error():
    # logs = db.session.query(Log.dataset).distinct()
    logs = db.session.query(Log.dataset, Log.logger).\
            group_by(Log.dataset, Log.logger).\
            order_by(Log.dataset)
    return jsonify(
            errored_datasets=[{'dataset': i[0], 'logger': i[1]} for i in logs.all()]
    )


@api.route('/error/resource/')
def resource_error():
    resource_url = request.args.get('url')
    if not resource_url:
        abort(404)
    error_logs = db.session.query(Log).\
        filter(Log.resource == resource_url).\
        order_by(sa.desc(Log.created_at))
    errors = [{
                'resource_url': log.resource,
                'dataset': log.dataset,
                'logger': log.logger,
                'msg': log.msg,
                'traceback': log.trace,
                'datestamp': log.created_at.isoformat(),
            } for log in error_logs.all()
    ]
    return jsonify(errors=errors)


@api.route('/error/dataset/<dataset_id>/')
def dataset_error(dataset_id):
    error_logs = db.session.query(Log).\
            filter(Log.dataset == dataset_id).\
            order_by(sa.desc(Log.created_at))
    errors = [{
                'resource_url': log.resource,
                'dataset': log.dataset,
                'logger': log.logger,
                'msg': log.msg,
                'traceback': log.trace,
                'datestamp': log.created_at.isoformat(),
            } for log in error_logs.all()]

    return jsonify(errors=errors)


@api.route('/error/dataset.log')
def dataset_log():
    logs = db.session.query(Log.dataset).distinct()
    response = make_response(
        render_template('datasets.log', logs=logs))
    response.mimetype = 'text/plain'
    return response


@api.route('/error/dataset.log/<dataset_id>/')
def dataset_log_error(dataset_id):
    error_logs = db.session.query(Log).\
        filter(Log.dataset == dataset_id).\
        order_by(Log.created_at.desc())
    errors = [{
        'resource_url': log.resource,
        'logger': log.logger,
        'msg': log.msg,
        'traceback': log.trace.split('\n') if log.trace else [],
        'datestamp': log.created_at.isoformat(),
    } for log in error_logs]

    response = make_response(
        render_template('dataset.log', errors=errors))
    response.mimetype = 'text/plain'
    return response


class Stream(object):
    """
    Wrapper to make a query object quack like a pagination object
    """

    limit = ''
    offset = ''

    def __init__(self, query):
        self.items = query
        self.total = query.count()


class DataStoreView(MethodView):
    filter = None
    serializer = None

    @property
    def streaming(self):
        return self.validate_args().get("stream", False)

    def paginate(self, query, offset, limit):
        if offset < 0:
            abort(404)
        items = query.order_by('iati_identifier').limit(limit).offset(offset).all()
        if not items and offset != 0:
            abort(404)
        return Scrollination(query, offset, limit, query.count(), items)

    def validate_args(self):
        if not hasattr(self, "_valid_args"):
            self._valid_args = validators.activity_api_args(MultiDict(request.args))
        return self._valid_args

    def get_response(self, serializer, mimetype):
        if serializer is None:
            serializer = self.serializer

        try:
            valid_args = self.validate_args()
        except (validators.MultipleInvalid, validators.Invalid) as e:
            return make_response(
                render_template('error/invalid_filter.html', errors=e), 400)
        query = self.filter(valid_args)

        if self.streaming:
            query = query.yield_per(100)
            body = serializer(Stream(query))
        else:
            pagination = self.paginate(
                query,
                valid_args.get("offset", 0),
                valid_args.get("limit", 50),
            )
            body = u"".join(list(serializer(pagination)))
        return Response(body, mimetype=mimetype)


class ActivityView(DataStoreView):
    filter = staticmethod(dsfilter.activities)

    def get(self, format):
        forms = {
            "xml": (serialize.xml, "application/xml"),
            "json": (serialize.json, "application/json"),  # rfc4627
            "db.json": (serialize.datastore_json, "application/json"),
            "csv": (serialize.csv, "text/csv")  # rfc4180
        }
        if format not in forms:
            abort(404)
        return self.get_response(*forms[format])


class DataStoreCSVView(DataStoreView):
    def get(self, format):
        if format != "csv":
            abort(404)
        return self.get_response(serializer=None, mimetype="text/csv")


class ActivityByCountryView(DataStoreCSVView):
    filter = staticmethod(dsfilter.activities_by_country)
    serializer = staticmethod(serialize.csv_activity_by_country)


class ActivityBySectorView(DataStoreCSVView):
    filter = staticmethod(dsfilter.activities_by_sector)
    serializer = staticmethod(serialize.csv_activity_by_sector)


class TransactionsView(DataStoreCSVView):
    filter = staticmethod(dsfilter.transactions)
    serializer = staticmethod(serialize.transaction_csv)


class TransactionsByCountryView(DataStoreCSVView):
    filter = staticmethod(dsfilter.transactions_by_country)
    serializer = staticmethod(serialize.csv_transaction_by_country)


class TransactionsBySectorView(DataStoreCSVView):
    filter = staticmethod(dsfilter.transactions_by_sector)
    serializer = staticmethod(serialize.csv_transaction_by_sector)


class BudgetsView(DataStoreCSVView):
    filter = staticmethod(dsfilter.budgets)
    serializer = staticmethod(serialize.budget_csv)


class BudgetsByCountryView(DataStoreCSVView):
    filter = staticmethod(dsfilter.budgets_by_country)
    serializer = staticmethod(serialize.csv_budget_by_country)


class BudgetsBySectorView(DataStoreCSVView):
    filter = staticmethod(dsfilter.budgets_by_sector)
    serializer = staticmethod(serialize.csv_budget_by_sector)


api.add_url_rule(
    '/access/activity/',
    defaults={"format": "json"},
    view_func=ActivityView.as_view('activity-view'),
)

api.add_url_rule(
    '/access/activity.<format>',
    view_func=ActivityView.as_view('activity')
)

api.add_url_rule(
    '/access/activity/by_country.<format>',
    view_func=ActivityByCountryView.as_view('activity_by_country'))

api.add_url_rule(
    '/access/activity/by_sector.<format>',
    view_func=ActivityBySectorView.as_view('activity_by_sector'))

api.add_url_rule(
    '/access/transaction.<format>',
    view_func=TransactionsView.as_view('transaction_list'))

api.add_url_rule(
    '/access/transaction/by_country.<format>',
    view_func=TransactionsByCountryView.as_view('transaction_by_country'))

api.add_url_rule(
    '/access/transaction/by_sector.<format>',
    view_func=TransactionsBySectorView.as_view('transaction_by_sector'))

api.add_url_rule(
    '/access/budget.<format>',
    view_func=BudgetsView.as_view('budget_list'))

api.add_url_rule(
    '/access/budget/by_country.<format>',
    view_func=BudgetsByCountryView.as_view('budget_by_country'))

api.add_url_rule(
    '/access/budget/by_sector.<format>',
    view_func=BudgetsBySectorView.as_view('budget_by_sector'))
