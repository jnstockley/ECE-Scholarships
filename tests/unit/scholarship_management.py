'''
Utilities for merging dfs
'''
import unittest
import pandas as pd
from src.utils.scholarship_management import read_rows, write_rows

class ScholarshipManagementTest(unittest.TestCase):
    def test_read_rows(self):
        '''
        Verify that rows are correctly read from a file
        '''
        rows = read_rows('tests/data/scholarships_test_file.xlsx')

        assert(not rows is None)
        assert(isinstance(rows, pd.DataFrame))

    def test_write_rows(self):
        '''
        Verify that rows are correctly wrote to a file
        '''
        scholarships = {'Name': ['Test Scholarship'], 'Total Amount': ['1000'], 'Value': ['2000'], 'RAI': ['315'],
                           'Admit Score': ['26'], 'Major': ['All'], 'ACT Math': ['25'], 'ACT English': ['27'],
                           'ACT Composite': ['25'], 'SAT Math': ['500'], 'SAT Reading': ['400'], 'SAT Combined': ['1000'],
                           'GPA': ['3.75'], 'HS Percentile': ['90'], 'Group One': [['ACT Math', 'SAT Math']],
                           'Group Two': [['ACT Composite', 'SAT Combined']], 'Group Three': [[]]}
        scholarships_df = pd.DataFrame(scholarships)
        write_rows(scholarships_df, 'tests/data/scholarships_test_file.xlsx', 'Scholarships')
        
        rows = read_rows('tests/data/scholarships_test_file.xlsx')
        
        assert(rows.shape[0] == 1)
        assert(rows['Name'][0] == 'Test Scholarship')
        assert(rows['ACT Math'][0] == 25)
        assert(rows['Group Two'][0] == "['ACT Composite', 'SAT Combined']")

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
