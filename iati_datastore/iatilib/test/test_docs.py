from os.path import dirname, realpath, join
import subprocess

from . import AppTestCase


class TestDocs(AppTestCase):
    def setUp(self):
        super().setUp()
        self.client = self.app.test_client()
        current_path = dirname(dirname(dirname(realpath(__file__))))
        cwd = join(current_path, 'docs_source')
        subprocess.run(['make', 'dirhtml'], cwd=cwd)

    def test_homepage_redirect(self):
        resp = self.client.get('/')
        self.assertEquals(302, resp.status_code)
        self.assertRegex(resp.headers['Location'], '/docs/$')

    def test_error_api_redirect(self):
        resp = self.client.get('/error/')
        self.assertEquals(302, resp.status_code)
        self.assertRegex(resp.headers['Location'], '/docs/api/error/$')

    def test_docs(self):
        resp = self.client.get('/docs/')
        self.assertEquals(200, resp.status_code)
        self.assertRegex(
            resp.data.decode(),
            r"What is IATI Datastore\?")

    def test_favicon(self):
        resp = self.client.get('/favicon.ico')
        self.assertEquals(200, resp.status_code)
        self.assertRegex(resp.content_type, "^image/")
