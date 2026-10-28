import json
from datetime import datetime
from unittest import TestCase, skipIf

import flask
import responses

from gitmostwanted.app import db
from gitmostwanted.blueprints.user_oauth import login, url_next
from gitmostwanted.models.repo import Repo, RepoMean, RepoTopics
from gitmostwanted.models.user import User
from gitmostwanted.web import app


class WebTestCase(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()

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

    def test_top_by_topic(self):
        topic = 'python'
        repo_matched = Repo(
            id=101, full_name='org/matched', name='matched', html_url='https://example.com/1',
            created_at=datetime.now(), mature=True, worth_max=9, worth=9, stargazers_count=100,
            topics=[RepoTopics(id=1, title=topic)]
        )
        repo_other = Repo(
            id=102, full_name='org/other', name='other', html_url='https://example.com/2',
            created_at=datetime.now(), mature=True, worth_max=9, worth=9, stargazers_count=200,
            topics=[RepoTopics(id=2, title='golang')]
        )
        db.session.add_all([repo_matched, repo_other])
        db.session.commit()

        details = self.app.get('/repository/details/101').data.decode('utf-8')
        self.assertIn('/topic/{}/'.format(topic), details)

        body = self.app.get('/topic/{}/'.format(topic)).data.decode('utf-8')
        self.assertIn(repo_matched.full_name, body)
        self.assertNotIn(repo_other.full_name, body)

        db.session.delete(repo_matched)
        db.session.delete(repo_other)
        db.session.commit()

    def test_top_discovery_and_momentum_ranking(self):
        worth = 8
        velocity = 14.5
        passive = Repo(
            id=103, full_name='org/passive', name='passive', html_url='https://example.com/3',
            created_at=datetime.now(), mature=True, worth_max=worth, worth=worth,
            stargazers_count=5000, forks_count=10, subscribers_count=5
        )
        emerging = Repo(
            id=104, full_name='org/emerging', name='emerging', html_url='https://example.com/4',
            created_at=datetime.now(), mature=True, worth_max=worth, worth=worth,
            stargazers_count=300, forks_count=80, subscribers_count=40
        )
        mean = RepoMean(repo_id=emerging.id, value=velocity)
        db.session.add_all([passive, emerging, mean])
        db.session.commit()

        wanted = self.app.get('/').data.decode('utf-8')
        self.assertLess(wanted.index(emerging.full_name), wanted.index(passive.full_name))
        self.assertIn('+{}/d'.format(velocity), wanted)
        self.assertIn('<span>{}</span>'.format(worth), wanted)

        momentum = self.app.get('/top/momentum/').data.decode('utf-8')
        self.assertIn('The fastest growing repositories (solid)', momentum)
        self.assertLess(momentum.index(emerging.full_name), momentum.index(passive.full_name))

        db.session.delete(mean)
        db.session.delete(passive)
        db.session.delete(emerging)
        db.session.commit()

    def test_trending_ranges(self):
        for rng in ['week', 'month', 'quarter', 'year']:
            res = self.app.get('/trending/{}'.format(rng), follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Trending ({})'.format(rng), res.data.decode('utf-8'))

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

    def test_repository_add_requires_auth(self):
        self.assertEqual(
            self.app.post('/repository', data={'full_name': 'org/repo'}).status_code, 403
        )

    @responses.activate
    def test_repository_add(self):
        user = User(github_id=1001, username='submitter', email='sub@example.com')
        db.session.add(user)
        db.session.commit()
        prefix = 'a' * 30
        payload = {
            'id': 501,
            'name': 'awesome-tool',
            'full_name': 'org/awesome-tool',
            'html_url': 'https://github.com/org/awesome-tool',
            'description': 'An awesome tool',
            'homepage': 'https://example.com',
            'language': 'Python',
            'created_at': '2024-01-15T10:00:00Z',
            'stargazers_count': 250,
            'forks_count': 15,
            'open_issues_count': 3,
            'size': 512,
            'subscribers_count': 12,
            'fork': False,
            'archived': False,
            'disabled': False,
            'license': {'key': 'mit'},
            'topics': ['python', 'cli', prefix + '-first', prefix + '-second']
        }
        responses.add(
            responses.GET, 'https://api.github.com/repos/{}'.format(payload['full_name']),
            status=200, body=json.dumps(payload), content_type='application/json'
        )
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = user.id
            res = client.post(
                '/repository',
                data={'full_name': payload['html_url']},
                headers={'Referer': 'https://evil.example.com/phish'},
                follow_redirects=False
            )
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.headers['Location'], '/')
            res = client.get('/', follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('The repository has been successfully added', res.data.decode('utf-8'))
            added = db.session.get(Repo, payload['id'])
            self.assertIsNotNone(added)
            self.assertEqual(added.full_name, payload['full_name'])
            self.assertEqual(added.stargazers_count, payload['stargazers_count'])
            self.assertEqual(added.license, payload['license']['key'])
            self.assertTrue(added.mature)
            self.assertEqual({t.title for t in added.topics}, {'python', 'cli', prefix})
            self.assertIn(
                'The repository is already in the database',
                client.post(
                    '/repository', data={'full_name': payload['full_name']}, follow_redirects=True
                ).data.decode('utf-8')
            )
            self.assertIn(
                'The repository name or URL is not valid',
                client.post(
                    '/repository', data={'full_name': 'not-a-repo'}, follow_redirects=True
                ).data.decode('utf-8')
            )
        db.session.delete(added)
        db.session.delete(user)
        db.session.commit()

    @responses.activate
    def test_repository_add_rejects_ineligible(self):
        user = User(github_id=1002, username='validator', email='val@example.com')
        db.session.add(user)
        db.session.commit()
        forked = 'org/forked-repo'
        small = 'org/small-repo'
        responses.add(
            responses.GET, 'https://api.github.com/repos/{}'.format(forked),
            status=200,
            body=json.dumps({'id': 502, 'full_name': forked, 'fork': True}),
            content_type='application/json'
        )
        responses.add(
            responses.GET, 'https://api.github.com/repos/{}'.format(small),
            status=200,
            body=json.dumps({
                'id': 503, 'full_name': small, 'fork': False, 'stargazers_count': 10
            }),
            content_type='application/json'
        )
        with self.app as client:
            with client.session_transaction() as sess:
                sess['user_id'] = user.id
            self.assertIn(
                'Forked, archived, or disabled repositories are not supported',
                client.post(
                    '/repository', data={'full_name': forked}, follow_redirects=True
                ).data.decode('utf-8')
            )
            self.assertIn(
                'The repository must have at least',
                client.post(
                    '/repository', data={'full_name': small}, follow_redirects=True
                ).data.decode('utf-8')
            )
        db.session.delete(user)
        db.session.commit()
