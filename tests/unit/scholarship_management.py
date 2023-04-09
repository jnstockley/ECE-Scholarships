'''
Utilities for merging dfs
'''
import unittest
import pandas as pd
from src.utils.scholarship_management import read_rows, write_rows, edit_row, groups_string_to_list, check_columns_equal

class ScholarshipManagementTest(unittest.TestCase):
    '''
    Unit Tests for src.utils.scholarship_management
    '''
    def setUp(self):
        self.scholarships = {'Name': ['Test Scholarship'], 'Total Amount': ['1000'], 'Value': ['2000'], 'RAI': ['315'],
                           'Admit Score': ['26'], 'Major': ['All'], 'ACT Math': ['25'], 'ACT English': ['27'],
                           'ACT Composite': ['25'], 'SAT Math': ['500'], 'SAT Reading': ['400'], 'SAT Combined': ['1000'],
                           'GPA': ['3.75'], 'HS Percentile': ['90'], 'Group One': [['ACT Math', 'SAT Math']],
                           'Group Two': [['ACT Composite', 'SAT Combined']], 'Group Three': [[]]}
        self.scholarships_df = pd.DataFrame(self.scholarships)

        self.columns = ['Name', 'Total Amount', 'Value', 'RAI', 'Admit Score', 'Major', 'ACT Math', 'ACT English',
                        'ACT Composite', 'SAT Math', 'SAT Reading', 'SAT Combined', 'GPA', 'HS Percentile', 
                        'Group One', 'Group Two', 'Group Three']
        self.columns_invalid = ['Name', 'Total Amount', 'Value', 'RAI', 'Admit Score', 'Major', 'ACT Math', 'ACT English',
                                'ACT Composite', 'SAT Math', 'Bad Column', 'SAT Reading', 'SAT Combined', 'GPA', 'HS Percentile', 
                                'Group One', 'Group Two', 'Group Three', 'Random Column']
        self.columns_missing = ['Name', 'Total Amount', 'RAI', 'Admit Score', 'Major', 'ACT Math', 'ACT English',
                                'ACT Composite', 'SAT Math', 'SAT Reading', 'GPA', 'HS Percentile', 
                                'Group One', 'Group Three']

    def test_read_rows(self):
        '''
        Verify that rows are correctly read from a file
        '''
        rows = read_rows('tests/data/scholarships_test_file.xlsx')

        assert not rows is None
        assert isinstance(rows, pd.DataFrame)

    def test_write_rows(self):
        '''
        Verify that rows are correctly wrote to a file
        '''
        write_rows(self.scholarships_df, 'tests/data/scholarships_test_file.xlsx', 'Scholarships')

        rows = read_rows('tests/data/scholarships_test_file.xlsx')

        assert rows.shape[0] == 1
        assert rows['Name'][0] == 'Test Scholarship'
        assert rows['ACT Math'][0] == 25
        assert rows['Group Two'][0] == str(['ACT Composite', 'SAT Combined'])
        assert rows['Group Three'][0] == str([])

    def test_edit_row(self):
        '''
        Verify that a row in a dataframe is correctly edited
        '''
        edit_row(self.scholarships_df, 0, [('Total Amount', '1500'), ('Group Three', str(['RAI', 'Admit Score']))])

        assert self.scholarships_df['Name'][0] == 'Test Scholarship'
        assert self.scholarships_df['Total Amount'][0] == '1500'
        assert self.scholarships_df['Group Three'][0] == str(['RAI', 'Admit Score'])

    def test_read_edit_write_rows(self):
        '''
        Verify that all of the functionality works together
        '''
        rows = read_rows('tests/data/scholarships_test_file.xlsx')
        edit_row(rows, 0, [('Total Amount', '1500'), ('Group Three', str(['RAI', 'Admit Score']))])
        write_rows(rows, 'tests/data/scholarships_test_file.xlsx', 'Scholarships')
        new_rows =  read_rows('tests/data/scholarships_test_file.xlsx')

        assert new_rows.shape[0] == 1
        assert rows['Name'][0] == 'Test Scholarship'
        assert rows['Total Amount'][0] == '1500'
        assert rows['ACT Math'][0] == 25
        assert rows['Group Two'][0] == str(['ACT Composite', 'SAT Combined'])
        assert rows['Group Three'][0] == str(['RAI', 'Admit Score'])

    def test_groups_string_to_list(self):
        '''
        Verify that groups_strings_to_list correctly converts data from a
        list as a string to the list object
        '''
        group_one = str(['ACT Composite', 'SAT Combined'])
        group_two = str([])
        new_group_one = groups_string_to_list(group_one)
        new_group_two = groups_string_to_list(group_two)

        assert new_group_one == ['ACT Composite', 'SAT Combined']
        assert new_group_two == []
    
    def test_check_columns_equal_correct(self):
        '''
        Verify that there are no errors when the columns are correct
        '''
        fail_columns, invalid_columns, missing_columns = check_columns_equal(self.columns, self.columns)

        assert fail_columns == 0
        assert invalid_columns == []
        assert missing_columns == []
    
    def test_check_columns_equal_invalid(self):
        fail_columns, invalid_columns, missing_columns = check_columns_equal(self.columns, self.columns_invalid)
        assert fail_columns == 2
        assert invalid_columns == ['Bad Column', 'Random Column']
        assert missing_columns == []
    
    # def test_check_columns_equal_missing(self):
    #     return
    
    # def test_check_columns_equal_invalid_missing(self):
    #     return

if __name__ == '__main__':
    unittest.main()
