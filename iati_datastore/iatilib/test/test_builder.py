from . import ClientTestCase


class TestLatestApiRedirect(ClientTestCase):
    def test_builder_errors(self):
        resp = self.client.get(
            '/build/api/1/access/nonsense/')
        self.assertEquals(404, resp.status_code)
        resp = self.client.get(
            '/build/api/1/access/activity/nonsense/')
        self.assertEquals(404, resp.status_code)
        resp = self.client.get(
            '/build/api/1/access/activity/by_country.nonsense')
        self.assertEquals(404, resp.status_code)

    def test_builder_activity_xml(self):
        url_from = '/build/api/1/access/activity.xml'
        url_to = '/'
        resp = self.client.get(url_from)
        self.assertEquals(302, resp.status_code)
        self.assertTrue(resp.headers['Location'].endswith(url_to))

    def test_builder_transaction_json(self):
        url_from = '/build/api/1/access/transaction.csv'
        url_to = '/?breakdown=transaction&format=csv'
        resp = self.client.get(url_from)
        self.assertEquals(302, resp.status_code)
        self.assertTrue(resp.headers['Location'].endswith(url_to))
