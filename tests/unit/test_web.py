from unittest import TestCase
from gitmostwanted.web import app, url_next, oauth_login


class WebTestCase(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_homepage(self):
        rv = self.app.get('/')
        assert '<title>gitmostwanted</title>' in rv.data.decode('utf-8')

    def test_oauth_login(self):
        with app.test_request_context():
            resp = oauth_login()
            self.assertTrue(resp.headers['Location'].endswith('authorized'))
            self.assertEquals(resp.status_code, 302)

    def test_provide_correct_redirect_url(self):
        env_overrides = dict(HTTP_REFERER='http_referer')
        with app.test_request_context(environ_overrides=env_overrides):
            self.assertTrue(url_next().endswith('http_referer'))
        with app.test_request_context('/?next=url_next'):
            self.assertTrue(url_next().endswith('url_next'))
        with app.test_request_context():
            self.assertIsNone(url_next())
