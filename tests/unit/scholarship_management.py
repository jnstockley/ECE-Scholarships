'''
Utilities for merging dfs
'''
import unittest
import pandas as pd
from src.utils.scholarship_management import read_rows

class ScholarshipManagementTest(unittest.TestCase):
    def test_read_rows(self):
        '''
        Verify that rows are correctly read from a file
        '''
        rows = read_rows('tests/data/scholarships_test_file.xlsx')

        assert(not rows is None)
        assert(isinstance(rows, pd.DataFrame))

    # def test_write_rows(self):
    #     return
    # def test_edit_row(self):
    #     return
    # def test_read_write_rows(self):
    #     return
    # def test_read_edit_write_rows(self):
    #     return
    # def test_groups_string_to_list(self):
    #     return

if __name__ == '__main__':
    unittest.main()
