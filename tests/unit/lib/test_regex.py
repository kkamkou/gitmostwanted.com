from unittest import TestCase
from gitmostwanted.lib.regex import SearchTerm


class LibRegexSearchTermTestCase(TestCase):
    def test_detect_valid_input(self):
        self.assertRaises(ValueError, SearchTerm, '#')
        self.assertRaises(ValueError, SearchTerm, 'te')
        self.assertEqual('%test%', str(SearchTerm('test')))
        self.assertEqual('%dot.%', str(SearchTerm('dot.')))
        self.assertEqual('%free-programming-books%', str(SearchTerm('free-programming-books')))
