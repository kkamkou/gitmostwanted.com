from unittest import TestCase

from gitmostwanted.lib.regex import RepoFullName, SearchTerm


class LibRegexSearchTermTestCase(TestCase):
    def test_detect_valid_input(self):
        self.assertRaises(ValueError, SearchTerm, '#')
        self.assertRaises(ValueError, SearchTerm, 'te')
        self.assertEqual('%test%', str(SearchTerm('test')))
        self.assertEqual('%dot.%', str(SearchTerm('dot.')))
        self.assertEqual('%free-programming-books%', str(SearchTerm('free-programming-books')))


class LibRegexRepoFullNameTestCase(TestCase):
    def test_detect_valid_full_name(self):
        expected = 'kkamkou/gitmostwanted.com'
        self.assertEqual(expected, str(RepoFullName(expected)))
        self.assertEqual(expected, str(RepoFullName('https://github.com/{}/'.format(expected))))
        self.assertEqual(
            expected, str(RepoFullName('  https://www.github.com/{}.git '.format(expected)))
        )
        self.assertRaises(ValueError, RepoFullName, '')
        self.assertRaises(ValueError, RepoFullName, 'invalid')
        self.assertRaises(ValueError, RepoFullName, 'github.com/owner')
        self.assertRaises(ValueError, RepoFullName, 'gitlab.com/owner')
        self.assertRaises(ValueError, RepoFullName, 'https://gitlab.com/owner/repo')
        self.assertRaises(ValueError, RepoFullName, '../..')
