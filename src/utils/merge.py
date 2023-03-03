'''
Several merging functions needed for combining dataframes.
'''
import pandas as pd

def align_dfs_along_columns(alignment_columns: list[str], dfs: list[pd.DataFrame]) -> pd.DataFrame:
    '''
    Combines multiple dataframes given a set of "alignment columns" where alignment columns
    continue unique data that will be present  between dataframes. Only unique row data (within the alignment columns) present
    in all dataframes will be included in the output df.

    Parameters
    ----------
    alignment_columns : list[str]
        Column strings present in all dataframes
    dfs : list[pd.DataFrame]
        Input dataframes

    Returns
    -------
    The new merged dataframe
    '''
    def get_case_sensitive_column(column, columns):
        '''
        Return the case sensitive column from a non-case sensitive column.
        '''
        for col in columns:
            if col.lower() == column.lower():
                return col

        return None

    # We do not care about case sensitivity
    alignment_columns = [col.lower() for col in alignment_columns]
    series_references = []

    for data in dfs:
        prev_length = len(series_references)

        for column in alignment_columns:
            if column.lower() in [col.lower() for col in data.columns]:
                case_sensitive_column = get_case_sensitive_column(column, data.columns)
                series_references.append(data[case_sensitive_column])

        if prev_length == len(series_references):
            raise RuntimeError(f'No valid match from {alignment_columns} found for dataframe columns: {data.columns}')

    print(series_references)
