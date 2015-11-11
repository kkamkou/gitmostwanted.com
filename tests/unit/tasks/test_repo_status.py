from gitmostwanted.tasks.repo_status import result_normalize, result_split
from types import GeneratorType
from unittest import TestCase


class TasksRepoStatusTestCase(TestCase):
    def test_normalize_result(self):
        result = result_normalize([[8, 8], [28, 28]], 28)
        self.assertIsInstance(result, GeneratorType)

        lst = list(result)
        self.assertEquals(lst[0], 8)
        self.assertEquals(lst[20], 28)
        self.assertEquals(len(lst), 28)

    def test_split_result(self):
        result = result_split(list(range(28)), 7)
        self.assertIsInstance(result, GeneratorType)

        lst = list(result)
        self.assertEquals(len(lst), 4)
        self.assertEquals(len(lst[0]), 7)
