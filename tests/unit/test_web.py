from unittest import TestCase
from gitmostwanted.web import app


class WebTestCase(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_homepage(self):
        rv = self.app.get('/')
        assert '<title>gitmostwanted</title>' in rv.data.decode('utf-8')
