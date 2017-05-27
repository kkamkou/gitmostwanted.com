from unittest import TestCase
from gitmostwanted.lib.url import Url


class LibUrlTestCase(TestCase):
    def test_strip_spaces(self):
        self.assertEqual(str(Url(' https://example.com ')), 'https://example.com')

    def test_restore_schema(self):
        self.assertEqual(str(Url('httpexample.com')), 'http://httpexample.com')
