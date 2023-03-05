'''
Several merging functions needed for combining dataframes.
'''
import pandas as pd

def combine_data(_alignment_columns, _aligned_row, _dfs: list[pd.DataFrame]):
    '''
    Test
    '''

def find_duplicates(alignment_columns: list[str], alignment_row_data, dfs: list[(str, pd.DataFrame)]) -> pd.DataFrame:
    '''
    Given alignment columns to reference and a set of dataframes which contains one of the alignment columns
    and atleast one dataframe that has the alignment row data provided within its alignment_column, this will check
    to see if any other dataframes containing that alignment row data in their alignment column has duplicate columns with varing data
    and if so, return a dataframe with those conflict rows.
    '''
    matches = []

    for data in dfs:
        for col in alignment_columns:
            if col in data.columns:
                col_data = data[col].tolist()
                if col_data.count(alignment_row_data) == 1:
                    matches.append(data.loc[data[col] == alignment_row_data,:])
                    print(matches[-1].head())
                    #match found, no need to check other alignment_columns.
                    break

    # Key = the column name, value = ... ?
    _common_columns = {}

    while len(matches) > 1:
        duplicates = set.intersection(*[set(match.columns) for match in matches])
        _differing_values = {}

        # Drop df references with no more duplicates
        for match in list(matches):
            local_duplicates = set.intersection(duplicates, set(match.columns))
            if len(local_duplicates) == 0:
                matches.remove(match)

        for _duplicate in duplicates:
            pass

def combine_columns(columns: list[pd.Series], drop_missing: bool) -> pd.Series:
    '''
    Combine several column series into 1. If drop_missing is flagged then only the values
    present in each column will be kept in output.
    '''
    sets = [set(col) for col in columns]
    if drop_missing:
        common_rows = set.intersection(*sets)
        return pd.Series(list(common_rows))

    all_unique_rows = set.union(*sets)
    return pd.Series(list(all_unique_rows))
