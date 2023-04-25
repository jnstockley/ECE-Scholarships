'''
Utilities for merging dfs
'''
import unittest
import pandas as pd
from utils import merge

class MergingDataframesTest(unittest.TestCase):
    '''
    Example UnitTest
    '''

    def test_combine_columns_with_no_drop_missing(self):
        '''
        Verify columns can be merged with no drop missing
        '''
        series1 = pd.Series(range(0,4,1))
        series2 = pd.Series(range(2,6,1))

        result = merge.combine_columns([series1, series2], False)
        result_list = result.tolist()

        assert len(result_list) == 6
        assert set(result_list) == set(range(0,6,1))

    def test_combine_columns_with_drop_missing(self):
        '''
        Verify columns can be merged with no drop missing
        '''
        series1 = pd.Series(range(0,4,1))
        series2 = pd.Series(range(2,6,1))

        result = merge.combine_columns([series1, series2], True)
        result_list = result.tolist()

        assert len(result_list) == 2
        assert set(result_list) == set(range(2,4,1))

if __name__ == '__main__':
    unittest.main()
