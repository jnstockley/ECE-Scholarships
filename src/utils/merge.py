'''
Several merging functions needed for combining dataframes.
'''
import pandas as pd

def align_dfs_along_columns(alignment_columns: list[str], _dfs: list[pd.DataFrame]) -> pd.DataFrame:
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

    for _column in alignment_columns:
        pass
