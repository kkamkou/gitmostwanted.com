from gitmostwanted.tasks.repo_status import result_normalize, result_split, result_mean
from types import GeneratorType
from unittest import TestCase
from itertools import chain


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

    def test_calculate_mean(self):
        def gn_normal():
            yield [10, 20]

        def gn_mixed():
            yield [10, 99999, 10]

        self.assertEquals(result_mean(gn_normal(), 1), 15)
        self.assertEquals(result_mean(gn_mixed(), 1), 1)
        self.assertEquals(result_mean(gn_mixed(), 10), 10)
        self.assertEquals(result_mean(chain(gn_mixed(), gn_normal()), 1), 8)
