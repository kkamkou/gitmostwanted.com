from unittest import TestCase
from gitmostwanted.github import api
import responses
import json


class GithubApiTestCase(TestCase):
    @responses.activate
    def test_understand_repo_info(self):
        responses.add(
            responses.GET, 'https://api.github.com/repos/kkamkou/gitmostwanted.com', status=200,
            body=json.dumps(self._body_repo_info()), content_type='application/json'
        )
        self.assertTupleEqual(
            api.repo_info('kkamkou/gitmostwanted.com'), (self._body_repo_info(), 200)
        )
        responses.add(
            responses.GET, 'https://api.github.com/repos/nobody/nothing', status=404,
            body=json.dumps(self._body_not_found()), content_type='application/json'
        )
        self.assertTupleEqual(api.repo_info('nobody/nothing'), (None, 404))

    @responses.activate
    def test_understand_rate_limit(self):
        responses.add(
            responses.GET, 'https://api.github.com/rate_limit', status=200,
            body=json.dumps(self._body_rate_limit()), content_type='application/json'
        )
        self.assertTupleEqual(api.rate_limit(), (self._body_rate_limit(), 200))

    def _body_rate_limit(self):
        return {
            'resources': {
                'search': {'limit': 30, 'remaining': 30, 'reset': 1441014241},
                'core': {'limit': 5000, 'remaining': 4999, 'reset': 1441016777}
            },
            'rate': {'limit': 5000, 'remaining': 4999, 'reset': 1441016777}
        }

    def _body_repo_info(self):
        {
            'id': 31981526,
            'name': 'gitmostwanted.com',
            'full_name': 'kkamkou/gitmostwanted.com',
            'html_url': 'https://github.com/kkamkou/gitmostwanted.com',
            'description': 'Advanced explorer of github.com',
            'watchers_count': 3,
            'language': 'Python',
            'watchers': 3,
        }

    def _body_not_found(self):
        return {
            'message': 'Not Found',
            'documentation_url': 'https://developer.github.com/v3'
        }
