from unittest import TestCase
from gitmostwanted.lib.text import TextWithoutSmilies, TextNormalized


class LibTextWithoutSmiliesTestCase(TestCase):
    def test_filter_smilies(self):
        tpls = ['a {} b', '{} a b', 'a b {}']
        for smile in [':point_up_2:', ':expressionless:', ':-1:']:
            for tpl in tpls:
                self.assertEqual('a b', str(TextWithoutSmilies(tpl.format(smile))))
        self.assertEqual(':hallo world:', str(TextWithoutSmilies(':hallo world:')))


class LibTextNormalizeTestCase(TestCase):
    def test_filter_invalid_chars(self):
        text = 'hello {} world'.format(u'\u0061\u0301')
        self.assertEqual('hello á world', str(TextNormalized(text)))
        text = '\xF0\x9F\x8E\xB7\xF0\x9F...'
        self.assertEqual('ð\x9f\x8e·ð\x9f...', str(TextNormalized(text)))
