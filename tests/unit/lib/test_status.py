from unittest import TestCase
from gitmostwanted.lib.status import Status


class LibStatusTestCase(TestCase):
    def test_create_new_object(self):
        self.assertEqual(str(Status('promising')), 'promising')

    def test_raise_on_incorrect_status(self):
        self.assertRaises(ValueError, Status, 'invalid_status')
