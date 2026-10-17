from unittest import TestCase, skipIf

import flask

from gitmostwanted.app import db
from gitmostwanted.blueprints.user_oauth import login, url_next
from gitmostwanted.models.user import User
from gitmostwanted.web import app


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
            '<title>The most interesting repositories (solid) - GitHub Explore</title>',
            self.app.get('/').data.decode('utf-8')
        )

    @skipIf('OAUTH_GITHUB' not in app.config, "Requires GitHub auth")
    def test_login_via_github(self):
        with app.test_request_context():
            resp = login()
            self.assertTrue(resp.headers['Location'].endswith('authorized'))
            self.assertEqual(resp.status_code, 302)

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
                session['oauth_access_token'] = 'oauth_access_token'
                session['user_id'] = 'user_id'
            self.assertIsInstance(a.get('/logout'), flask.Response)
            self.assertNotIn('oauth_access_token', flask.session)
            self.assertNotIn('user_id', flask.session)

    def test_load_user_from_session(self):
        user = User(github_id=999, username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()

        with self.app as c:
            with c.session_transaction() as sess:
                sess['user_id'] = user.id
            c.get('/')
            self.assertEqual(flask.g.user.id, user.id)
