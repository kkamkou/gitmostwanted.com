from unittest import TestCase
from gitmostwanted.lib.text import TextWithoutSmilies


class LibTextWithoutSmiliesTestCase(TestCase):
    def test_filter_smilies(self):
        tpls = ['a {} b', '{} a b', 'a b {}']
        for smile in [':point_up_2:', ':expressionless:', ':-1:']:
            for tpl in tpls:
                self.assertEquals('a b', str(TextWithoutSmilies(tpl.format(smile))))
        self.assertEquals(':hallo world:', str(TextWithoutSmilies(':hallo world:')))
