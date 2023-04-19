'''
Functions that are used in scholarship_management.py page
Some of these are relatively general pandas dataframe functions
'''
import pandas as pd

def read_rows(file_path):
    '''
    Reads excel spreasheet and returns the rows
    NOTE: needs to be changed for sharepoint
    '''
    excel = pd.read_excel(file_path)
    return excel.head()

def write_rows(dataframe, file_path, sheet_name):
    '''
    Writes the rows of a dataframe to the file_path with sheet_name
    NOTE: needs to be changed for sharepoint
    '''
    dataframe.to_excel(file_path, sheet_name=sheet_name, index=False)

def edit_row(dataframe, row_index, column_names_and_values):
    '''
    Takes a row index and a list of tuples that contain the column name
    and the new column value and edits those values of the associated row
    in that dataframe
    '''
    for column_name, row_value in column_names_and_values:
        # loc takes in the row index and the column name and rewrites the value of that row and column
        dataframe.loc[row_index, column_name] = row_value

def groups_string_to_list(default_options):
    '''
    This function is for converting the groups read in from the pandas dataframe ('Group One', etc.) from a string
    to the original list they were. Example: ['ACT Composite', 'SAT Combined'] is converted to "['ACT Composite', 'SAT Combined']"
    when the data is read in, this function converts it back to ['ACT Composite', 'SAT Combined'].
    '''
    # Needed edge case for when there is no options
    if default_options == "[]":
        return []
    # Removes [] from the string
    no_brackets = default_options[1:(len(default_options)-1)]
    # Removes ' ' around the items in the group
    no_quotes = no_brackets.replace('\'', '')
    # Removes the ,_ from the string and places everything into the split list
    list_form = no_quotes.split(', ')
    return list_form

def check_columns_equal(old_columns, new_columns):
    '''
    This function is for determining if two lists of columns are equal, and if they are not,
    what the failures are. It separates invalid columns and missing columns since they are
    both different errors.
    '''
    # Tracker of how many failed columns there are
    fail_columns = 0
    invalid_columns = []
    missing_columns = []

    # Determine which columns are invalid
    for col in new_columns:
        if col not in old_columns:
            fail_columns += 1
            invalid_columns.append(col)
    # Determine which columns are missing
    for col in old_columns:
        if col not in new_columns:
            fail_columns += 1
            missing_columns.append(col)

    return fail_columns, invalid_columns, missing_columns

def equalize_dictionary_columns(columns, dict_to_change):
    '''
    This function takes a list of columns and a dictionary and if there are any columns
    that are not present in the dictionary as a key it adds them and gives them the value of None
    '''
    for val in columns:
        if val not in dict_to_change:
            dict_to_change[val] = None
    # This is not a necessary return statement but is kept for understanding
    return dict_to_change
