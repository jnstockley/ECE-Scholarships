'''
Several merging functions needed for combining dataframes.
'''
import pandas as pd

def find_columns_to_merge(_dfs: list[pd.DataFrame], _similarity: float) -> dict[str, list[str]]:
    '''
    Given a list of dataframes, finds columns similar between two or more

    Parameters
    ----------
        dfs : list[pd.Dataframe()]
            List of dataframes to merge.
        similarity : float
            Similarity is min threshold for how similar columns need to be to be merged.
    '''

def merge_dfs(_dfs: list[pd.DataFrame], _merge_columns: dict[str, list[str]]) -> pd.DataFrame:
    '''
    Given a list of dataframes, combines data (and merge columns if necessary)

    Parameters
    ----------
        dfs : list[pd.Dataframe()]
            List of dataframes to merge.
        merge_columns: dict[str, list[str]]
            Input columns to merge as a dictionary where key represents the column name in the outputted
            dataframe and value is a list of column names from the inputted dataframes you'd like to merge.
    Returns
    -------
        Merged dataframe
    '''

def find_similarity_scores(_name: str, _df: pd.DataFrame) -> list[tuple[str, float]]:
    '''
    Takes a column name and checks the columns of a dataframe to rank them on similarity
    to the column name.

    Parameters
    ----------
    name : str
        Column name to find similarity to
    df : pd.Dataframe
        Checks df columns and finds similarity score to name.

    Returns
    -------
        List of tuples with first value being the column name from df, and second value being the
        associated similarity with name input.
    '''
