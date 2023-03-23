'''
Merge similar columns related managers and state to simplify session management.
'''
import pandas as pd
import streamlit as st
from src.utils import merge

# Desired similarity score
SIMILARITY_SCORE = 60

class MergeSimilarDetails:
    '''
    Details about similar columns to merge.

    final_column_name : str
        The final column name to use if similar columns are merged
    similar_columns : list[str]
        List of similar columns.
    aligned_df : pd.DataFrame()
        The aligned dataframe.
    alignment_col : str
        Name of the alignment column
    '''
    def __init__(self, final_column_name: str, similar_columns: list[str], alignment_col: str, aligned_df: pd.DataFrame):
        self.final_column_name: str = final_column_name
        self.similar_columns: list[str] = similar_columns
        self.alignment_col = alignment_col
        self.aligned_df = aligned_df

    def get_similar_column_df(self):
        '''
        Returns a df of just the similar columns so they can be compared easily
        '''
        return self.aligned_df.loc[:, [self.alignment_col] + self.similar_columns]

    def get_merge_preview_df(self):
        '''
        Returns a preview of what the merged dataframe will look like if all similar columns are combined.
        '''
        final_column_data = []

        for column in self.similar_columns:
            data = self.aligned_df.loc[:, [self.alignment_col, column]].copy(deep=True)
            data.rename({"{column}": self.final_column_name}, inplace=True)
            final_column_data.append(data)

        merged_df: pd.DataFrame = final_column_data.pop()
        for remaining_data in final_column_data:
            merged_df = pd.merge(merged_df, remaining_data, on=self.alignment_col)

        return merged_df.loc[:, self.final_column_name]

    def get_comparison_table(self):
        '''
        Returns a table with only the rows that have differing values
        '''
        final_column_data = []

        for column in self.similar_columns:
            data = self.aligned_df.loc[:, [self.alignment_col, column]].copy(deep=True)
            data.rename({"{column}": self.final_column_name}, inplace=True)
            final_column_data.append(data)

        merged_df: pd.DataFrame = final_column_data.pop()
        for remaining_data in final_column_data:
            merged_df = pd.merge(merged_df, remaining_data, on=self.alignment_col)

        different_rows_mask = self._get_different_rows_mask()
        table = self.aligned_df.loc[different_rows_mask, [self.alignment_col] + self.similar_columns].copy(deep=True)
        table['FINAL COLUMN'] = merged_df.loc[different_rows_mask, self.final_column_name]

        return table

    def get_different_row_count(self) -> int:
        '''
        Returns count of the number of rows where similar column values vary
        '''
        return self._get_different_rows_mask().sum()

    def _get_different_rows_mask(self) -> pd.Series:
        '''
        Returns the pandas row mask for the alignment_df of which rows have values which deviate
        between the similar columns.
        '''
        def check_if_row_values_equal(row: pd.Series):
            unique_vals = row[self.similar_columns].unique()
            return len(unique_vals) > 1

        return self.aligned_df.apply(check_if_row_values_equal, axis=1)

class MergeSimilarManager:
    '''
    Manages the similar column merge flow for import UI.

    current_similar_columns : MergeSimilarDetails
        Current group of comparison columns to look at
    '''
    def __init__(self, alignment_col: str, aligned_df: pd.DataFrame):
        similar_columns = merge.find_similar_columns(aligned_df.columns.tolist(), SIMILARITY_SCORE)

        self._similarity_matches = []
        self.current_similar_columns = None

        for match in similar_columns:
            final_column = match[0]
            similar_columns = match[1] + [final_column]
            self._similarity_matches.append(MergeSimilarDetails(final_column, similar_columns, alignment_col, aligned_df))

    def has_group_to_handle(self) -> bool:
        '''
        Returns true if there is still a similar column group to handle
        '''
        return not self.current_similar_columns is None or self.remaining_count() > 0

    def get_column_group(self) -> MergeSimilarDetails:
        '''
        Returns next group of similar column details for the user to decide on.
        Will return same group until decision is made.
        '''
        if self.current_similar_columns:
            return self.current_similar_columns

        self.current_similar_columns = self._similarity_matches.pop()
        return self.current_similar_columns

    def remaining_count(self) -> int:
        '''
        Get # of remaining similar column groups to check
        '''
        return len(self._similarity_matches)

    def merge_columns(self):
        '''
        Select to merge the columns found in self.current_similar_columns
        '''

    def dont_merge_columns(self):
        '''
        Decide not to merge the similar column group find in self.current_similar_columns
        '''
        self.current_similar_columns = None
        st.experimental_rerun()
