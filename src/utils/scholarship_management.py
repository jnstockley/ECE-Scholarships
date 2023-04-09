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
    fail_columns = 0
    invalid_columns = []
    missing_columns = []

    for col in new_columns:
        if col not in old_columns:
            fail_columns += 1
            invalid_columns.append(col)
    for col in old_columns:
        if col not in new_columns:
            fail_columns += 1
            missing_columns.append(col)

    return fail_columns, invalid_columns, missing_columns