from unittest import TestCase
from gitmostwanted.app import env


class ConfigTestCase(TestCase):
    def test_detect_proper_env(self):
        self.assertEqual(env, 'Development')
