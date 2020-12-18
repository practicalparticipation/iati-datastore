import json
import datetime

import mock

from . import AppTestCase, fixture_filename
from . import factories as fac

from iatilib import crawler, db, parse
from iatilib.model import Dataset, Resource, Activity, DeletedActivity


class TestCrawler(AppTestCase):
    @mock.patch('iatikit.data')
    @mock.patch('glob.glob')
    def test_fetch_package_list(self, glob_mock, iatikit_mock):
        glob_mock.return_value = [
            "__iatikitcache__/registry/data/tst/tst-a.xml",
            "__iatikitcache__/registry/data/tst/tst-b.xml",
        ]
        data_mock = iatikit_mock.return_value
        data_mock.last_updated = datetime.datetime.utcnow()
        datasets = crawler.fetch_dataset_list()
        self.assertIn("tst-a", [ds.name for ds in datasets])
        self.assertIn("tst-b", [ds.name for ds in datasets])

    @mock.patch('iatikit.data')
    @mock.patch('glob.glob')
    def test_update_adds_datasets(self, glob_mock, iatikit_mock):
        glob_mock.return_value = [
            "__iatikitcache__/registry/data/tst/tst-a.xml",
        ]
        data_mock = iatikit_mock.return_value
        data_mock.last_updated = datetime.datetime.utcnow()
        datasets = crawler.fetch_dataset_list()
        glob_mock.return_value = [
            "__iatikitcache__/registry/data/tst/tst-a.xml",
            "__iatikitcache__/registry/data/tst/tst-b.xml",
        ]
        datasets = crawler.fetch_dataset_list()
        self.assertEquals(2, datasets.count())

    @mock.patch('iatikit.data')
    @mock.patch('glob.glob')
    def test_update_deletes_datasets(self, glob_mock, iatikit_mock):
        glob_mock.return_value = [
            "__iatikitcache__/registry/data/tst/tst-a.xml",
            "__iatikitcache__/registry/data/tst/tst-b.xml",
        ]
        data_mock = iatikit_mock.return_value
        data_mock.last_updated = datetime.datetime.utcnow()
        datasets = crawler.fetch_dataset_list()
        glob_mock.return_value = [
            "__iatikitcache__/registry/data/tst/tst-a.xml",
        ]
        datasets = crawler.fetch_dataset_list()
        self.assertEquals(1, datasets.count())

    def test_fetch_dataset(self):
        read_data = json.dumps({
            "resources": [{"url": "http://foo"}],
        })
        mock_open = mock.mock_open(read_data=read_data)
        with mock.patch('builtins.open', mock_open):
            dataset = crawler.fetch_dataset_metadata(Dataset())
        self.assertEquals(1, len(dataset.resources))
        self.assertEquals("http://foo", dataset.resources[0].url)

    def test_fetch_dataset_with_many_resources(self):
        read_data = json.dumps({
            "resources": [
                {"url": "http://foo"}, {"url": "http://bar"},
                {"url": "http://baz"},
            ]
        })
        mock_open = mock.mock_open(read_data=read_data)
        with mock.patch('builtins.open', mock_open):
            dataset = crawler.fetch_dataset_metadata(Dataset())
        self.assertEquals(3, len(dataset.resources))

    def test_fetch_dataset_count_commited_resources(self):
        read_data = json.dumps({
            "resources": [
                {"url": "http://foo"},
                {"url": "http://bar"},
                {"url": "http://baz"},
            ]
        })
        mock_open = mock.mock_open(read_data=read_data)
        with mock.patch('builtins.open', mock_open):
            crawler.fetch_dataset_metadata(Dataset(name="tstds"))
        db.session.commit()
        self.assertEquals(3, Resource.query.count())

    @mock.patch('iatikit.data')
    def test_fetch_resource_succ(self, iatikit_mock):
        data_mock = iatikit_mock.return_value
        data_mock.last_updated = datetime.datetime.utcnow()
        fac.DatasetFactory.create(
            name='tst-a',
            resources=[fac.ResourceFactory.create(
                url="http://foo",
            )]
        )
        read_data = b"test"
        mock_open = mock.mock_open(read_data=read_data)
        with mock.patch('builtins.open', mock_open):
            resource = crawler.fetch_resource(Resource(dataset_id="tst-a"))
        self.assertEquals(b"test", resource.document)
        self.assertEquals(None, resource.last_parsed)
        self.assertEquals(None, resource.last_parse_error)

    def test_parse_resource_succ(self):
        resource = Resource(document=b"<iati-activities />", url="http://foo")
        resource = crawler.parse_resource(resource)
        self.assertEquals([], list(resource.activities))
        self.assertEquals(None, resource.last_parse_error)
        now = datetime.datetime.utcnow()
        self.assertAlmostEquals(
            resource.last_parsed,
            now,
            delta=datetime.timedelta(seconds=15))

    def test_parse_resource_succ_replaces_activities(self):
        # what's in the db before the resource is updated
        act = fac.ActivityFactory.build(iati_identifier="deleted_activity")
        resource = fac.ResourceFactory.create(
            url="http://test",
            activities=[act]
        )
        # the updated resource (will remove the activities)
        resource.document = b"<iati-activities />"
        resource = crawler.parse_resource(resource)
        db.session.commit()
        self.assertEquals(None, Activity.query.get(act.iati_identifier))
        self.assertIn(
            "deleted_activity",
            [da.iati_identifier for da in DeletedActivity.query.all()]
        )

    def test_deleted_activity_removal(self):
        db.session.add(
            DeletedActivity(
                iati_identifier='test_deleted_activity',
                deletion_date=datetime.datetime(2000, 1, 1)))
        db.session.commit()
        resource = fac.ResourceFactory.create(
            url="http://test",
            document=b"""
                <iati-activities>
                  <iati-activity>
                    <iati-identifier>test_deleted_activity</iati-identifier>
                    <title>test_deleted_activity</title>
                    <reporting-org ref="GB-CHC-202918" type="21">Oxfam GB</reporting-org>
                  </iati-activity>
                </iati-activities>
            """,
        )
        self.assertIn(
            "test_deleted_activity",
            [da.iati_identifier for da in db.session.query(DeletedActivity).all()]
        )
        resource = crawler.parse_resource(resource)
        db.session.commit()
        self.assertNotIn(
            "test_deleted_activity",
            [da.iati_identifier for da in DeletedActivity.query.all()]
        )

    def test_last_changed_datetime(self):
        resource = fac.ResourceFactory.create(
            url="http://test",
            document=b"""
                <iati-activities>
                  <iati-activity>
                    <iati-identifier>test_deleted_activity</iati-identifier>
                    <title>test_deleted_activity</title>
                    <reporting-org ref="GB-CHC-202918" type="21">Oxfam GB</reporting-org>
                  </iati-activity>
                  <iati-activity>
                    <iati-identifier>test_deleted_activity_2</iati-identifier>
                    <title>test_deleted_activity_2</title>
                    <reporting-org ref="GB-CHC-202918" type="21">Oxfam GB</reporting-org>
                  </iati-activity>
                </iati-activities>
            """
        )
        crawler.parse_resource(resource)
        db.session.commit()
        db.session.query(Activity).update(
            values={'last_change_datetime': datetime.datetime(2000, 1, 1)},
            synchronize_session=False)
        db.session.commit()
        crawler.parse_resource(resource)
        acts = db.session.query(Activity).all()
        self.assertEquals(
            datetime.datetime(2000, 1, 1),
            acts[0].last_change_datetime)

    def test_parse_resource_fail(self):
        resource = Resource(document=b"", url="")
        with self.assertRaises(parse.ParserError):
            resource = crawler.parse_resource(resource)
            self.assertEquals(None, resource.last_parsed)

    @mock.patch('iatikit.data')
    @mock.patch('glob.glob')
    def test_deleted_activities(self, glob_mock, iatikit_mock):
        fac.DatasetFactory.create(
            name='deleteme',
            resources=[fac.ResourceFactory.create(
                url="http://yes",
                activities=[
                    fac.ActivityFactory.build(
                        iati_identifier="deleted_activity",
                        title="orig",
                    )
                ]
            )]
        )
        self.assertIn("deleteme", [ds.name for ds in Dataset.query.all()])
        data_mock = iatikit_mock.return_value
        data_mock.last_updated = datetime.datetime.utcnow()
        glob_mock.return_value = [
            "__iatikitcache__/registry/data/tst/tst-a.xml",
            "__iatikitcache__/registry/data/tst/tst-b.xml",
        ]
        datasets = crawler.fetch_dataset_list()
        self.assertNotIn("deleteme", [ds.name for ds in datasets])
        self.assertIn(
            "deleted_activity",
            [da.iati_identifier for da in DeletedActivity.query.all()]
        )

    def test_document_metadata(self):
        res = fac.ResourceFactory.create(
            url="http://res2",
            document=open(fixture_filename("complex_example_dfid.xml")).read().encode()
        )
        result = crawler.parse_resource(res)

        self.assertEquals("1.00", result.version)


class TestResourceUpdate(AppTestCase):
    def test_activity_in_two_resources(self):
        # If an activity is reported in two resources, the one in the db
        # wins.

        # Example: Activity GB-1-111635 appears in two resources.
        # 'http://projects.dfid.gov.uk/iati/Region/798'
        # 'http://projects.dfid.gov.uk/iati/Country/CD'

        # this resouce was the first to import activity "47045-ARM-202-G05-H-00"
        fac.DatasetFactory.create(
            name='tst-a',
            resources=[fac.ResourceFactory.create(
                url=u"http://res1",
                activities=[
                    fac.ActivityFactory.build(
                        iati_identifier=u"47045-ARM-202-G05-H-00",
                        title=u"orig",
                    )
                ]
            )]
        )

        # this resource has just been retrieved, it also contains an
        # activity "47045-ARM-202-G05-H-00"
        fac.DatasetFactory.create(
            name='tst-b',
            resources=[fac.ResourceFactory.create(
                url=u"http://res2",
                document=open(fixture_filename("single_activity.xml")).read().encode()
            )]
        )

        crawler.update_activities("tst-b")
        self.assertEquals(
            u"orig",
            Activity.query.get(u"47045-ARM-202-G05-H-00").title
        )
