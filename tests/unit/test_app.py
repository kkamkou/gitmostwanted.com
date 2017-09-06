from gitmostwanted import app
from unittest import TestCase


class AppTestCase(TestCase):
    def test_share_limited_set(self):
        for key in dir(app):
            if key.find('__') == 0:
                continue
            self.assertIn(key, ['sentry', 'app', 'env', 'celery', 'db', 'log'])
