from unittest import TestCase, skipIf
from gitmostwanted.web import app, url_next, oauth_login, db
import flask


class WebTestCase(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()

    def test_homepage(self):
        self.assertIn(
            '<title>Trending - Git Most Wanted (alpha)</title>',
            self.app.get('/').data.decode('utf-8')
        )

    @skipIf('OAUTH_GITHUB' not in app.config, "Requires GitHub auth")
    def test_login_via_github(self):
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

    def test_logout(self):
        with self.app as a:
            with self.app.session_transaction() as session:
                session['github_token'] = 'github_token'
                session['user_id'] = 'user_id'
            self.assertIsInstance(a.get('/logout'), flask.Response)
            self.assertNotIn('github_token', flask.session)
            self.assertNotIn('user_id', flask.session)
