import unittest

from powerset import format_output
from powerset import parse_input
from powerset import powerset_dfs
from powerset import powerset_iterative
from powerset import powerset_mp
from powerset import powerset_pythonic


class TestPowerset(unittest.TestCase):

    def test_parse_input(self):
        test_in = '1,2,3'
        expected_result = ['1', '2', '3']
        self.assertEqual(parse_input(test_in), expected_result, 'Input parser test failed!')

    def test_powerset_len(self):
        test_in = [1, 2, 3]
        self.assertEqual(len(list(powerset_pythonic(test_in))), pow(2, len(test_in)) - 1, "Length test failed!")

    def test_powerset_deep_comparison(self):
        test_in = [1, 2, 3]
        expected_result = [(1,), (2,), (3,), (1, 2,), (1, 3), (2, 3,), (1, 2, 3,)]
        self.assertListEqual(list(powerset_pythonic(test_in)), expected_result, 'Deep comparison failed!')

    def test_powerset_full(self):
        test_in = '123,456,789'
        expected_result = """123\n456\n789\n123,456\n123,789\n456,789\n123,456,789"""
        parsed_input = parse_input(test_in)
        powerset_out = powerset_pythonic(parsed_input)
        formatted_out = format_output(powerset_out)
        self.assertMultiLineEqual(formatted_out, expected_result)

    def test_dfs_powerset(self):
        test_in = [1, 2, 3, 4]
        expected_result = [[1], [2], [3], [4], [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4], [1, 2, 3], [1, 2, 4],
                           [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]
        self.assertCountEqual(powerset_dfs(test_in), expected_result, 'Deep comparison failed!')

    def test_powerset_mp(self):
        test_in = [1, 2, 3, 4]
        expected_result = [[1], [2], [3], [4], [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4], [1, 2, 3], [1, 2, 4],
                           [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]
        self.assertCountEqual(powerset_mp(test_in), expected_result,
                              'Deep comparison on multiprocessing version failed!')

    def test_powerset_iterative(self):
        test_in = [1, 2, 3, 4]
        expected_result = [[1], [2], [3], [4], [1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4], [1, 2, 3], [1, 2, 4],
                           [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]
        self.assertCountEqual(powerset_iterative(test_in), expected_result,
                              'Deep comparison on iterative version failed!')


if __name__ == '__main__':
    unittest.main()
