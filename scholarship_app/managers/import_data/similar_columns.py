"""
Merge similar columns related managers and state to simplify session management.
"""
from enum import Enum
import math
from typing import Callable
import pandas as pd
import numpy as np
import streamlit as st
from scholarship_app.utils import merge

# Desired similarity score
SIMILARITY_SCORE = 60


class StatusMessage(Enum):
    """
    Global shared sessions
    """

    CUSTOM_SCRIPT = "custom_script"


class MergeSimilarDetails:
    """
    Details about similar columns to merge.

    Attributes
    ----------
    final_column_name : str
        The final column name to use if similar columns are merged
    self.selected_columns : list[str]
        List of the selected columns (from the similar columns) that the user would like to merge.
    similar_columns : list[str]
        List of similar columns.
    aligned_df : pd.DataFrame()
        The aligned dataframe.
    alignment_col : str
        Name of the alignment column
    status_messages : dict[str, str]
    _merge_row_callback : Callable[[np.ndarray], any]
        Custom code written by user to execute per column of the merge DF
    """

    def __init__(
        self,
        final_column_name: str,
        similar_columns: list[str],
        alignment_col: str,
        aligned_df: pd.DataFrame,
    ):
        self.final_column_name: str = final_column_name
        self.selected_columns: list[str] = similar_columns
        self.similar_columns: list[str] = similar_columns
        self.alignment_col = alignment_col
        self.aligned_df = aligned_df
        self._merge_row_callback = self._default_merge_lambda
        self.status_messages = {}

    def set_selected_columns(self, selected: list[str]):
        """
        Updates the list of selected columns from the similar columns that the user would actually like to merge.
        """
        # Final column name may have been the column that was removed causing issues when creating merged df
        if self.final_column_name not in selected:
            self.final_column_name = selected[0]

        self.selected_columns = selected
        st.experimental_rerun()

    def apply_custom_merge_script(self, script: str):
        """
        Takes the custom merge row script and applys it to the DF
        """
        my_globals = {}
        my_locals = {}

        exec(script, my_globals, my_locals)

        # Extract the function object from the locals dictionary
        callback_func = my_locals["merge"]

        # Test for any runtime errors
        self._get_merged_df(callback_func)

        self._merge_row_callback = callback_func
        self.status_messages[
            StatusMessage.CUSTOM_SCRIPT
        ] = "Changes successfully saved! The FINAL COLUMN above is now updated!"
        st.experimental_rerun()

    def reset_custom_merge_script(self):
        """
        Sets the merge row callback to the default merge row callback function.
        """
        self._merge_row_callback = self._default_merge_lambda
        self.status_messages[
            StatusMessage.CUSTOM_SCRIPT
        ] = "FINAL COLUMN has been reset to the default merge technique!"
        st.experimental_rerun()

    def get_similar_column_df(self):
        """
        Returns a df of just the similar columns so they can be compared easily
        """
        return self.aligned_df.loc[:, [self.alignment_col] + self.similar_columns]

    def set_final_column_name(self, name: str):
        """
        Set final column name
        """
        self.final_column_name = name

    def get_merge_preview_df(self):
        """
        Returns a preview of what the merged dataframe will look like if all similar columns are combined.
        """
        merged_df = self._get_merged_df(self._merge_row_callback)

        return merged_df.loc[:, self.final_column_name]

    def get_comparison_table(self):
        """
        Returns a table with only the rows that have differing values
        """
        merged_df = self._get_merged_df(self._merge_row_callback)

        different_rows_mask = self._get_different_rows_mask()
        table = self.aligned_df.loc[
            different_rows_mask, [self.alignment_col] + self.selected_columns
        ].copy(deep=True)
        table["FINAL COLUMN"] = merged_df.loc[
            different_rows_mask, self.final_column_name
        ]

        return table

    def perform_merge(self, final_col: pd.Series) -> set[str]:
        """
        Removes the associated similar columns, adds new column to db
        with name being final_column_name

        Returns
        -------
        Set of all the columns that need to be dropped from df when all similar columns
        have been addressed.
        """
        merged_df = self._get_merged_df(self._merge_row_callback)
        merged_df.loc[final_col.index, self.final_column_name] = final_col

        drop_cols = set(self.similar_columns)
        if self.final_column_name in drop_cols:
            drop_cols.remove(self.final_column_name)

        self.aligned_df.loc[:, self.final_column_name] = merged_df[
            self.final_column_name
        ]
        return drop_cols

    def get_different_row_count(self) -> int:
        """
        Returns count of the number of rows where similar column values vary
        """
        return self._get_different_rows_mask().sum()

    def _get_different_rows_mask(self) -> pd.Series:
        """
        Returns the pandas row mask for the alignment_df of which rows have values which deviate
        between the similar columns.
        """

        def check_if_row_values_equal(row: pd.Series):
            unique_vals = row[self.selected_columns].unique()
            return len(unique_vals) > 1

        return self.aligned_df.apply(check_if_row_values_equal, axis=1)

    def _default_merge_lambda(self, row):
        values: list[any] = row.tolist()
        values.remove(row[self.alignment_col])

        common_val = row[self.final_column_name]
        max_count = 0

        if not (
            common_val is None
            or (type(common_val) in [int, float] and math.isnan(common_val))
        ):
            max_count = 1

        for val in values:
            if val is None or (type(val) in [int, float] and math.isnan(val)):
                continue

            rel_count = values.count(val)

            if rel_count > max_count:
                max_count = rel_count
                common_val = val

        return common_val

    def _get_merged_df(self, method: Callable[[np.ndarray], any]) -> pd.DataFrame:
        """
        Returns the merged alignment dataframe if the similar column names were
        combined together.

        method:
            The lambda function to apply to each row of the dataframe in order to get
            the preview of the final merged column.
        """
        merged_df = self.aligned_df.loc[
            :, self.selected_columns + [self.alignment_col]
        ].copy(deep=True)
        merged_df[self.final_column_name] = merged_df.apply(method, axis=1)

        return merged_df.loc[:, [self.alignment_col, self.final_column_name]]


class MergeSimilarManager:
    """
    Manages the similar column merge flow for import UI.

    current_similar_columns : MergeSimilarDetails
        Current group of comparison columns to look at
    columns_to_remove : set[str]
        columns to be dropped from alignment df at end of all similar column groups being merged.
    """

    def __init__(self, alignment_col: str, aligned_df: pd.DataFrame):
        similar_columns = merge.find_similar_columns(
            aligned_df.columns.tolist(), SIMILARITY_SCORE
        )

        self._similarity_matches = []
        self.columns_to_remove: set[str] = set()
        self.current_similar_columns = None

        for match in similar_columns:
            final_column = match[0]
            similar_columns = match[1] + [final_column]
            self._similarity_matches.append(
                MergeSimilarDetails(
                    final_column, similar_columns, alignment_col, aligned_df
                )
            )

    def has_group_to_handle(self) -> bool:
        """
        Returns true if there is still a similar column group to handle
        """
        return not self.current_similar_columns is None or self.remaining_count() > 0

    def get_column_group(self) -> MergeSimilarDetails:
        """
        Returns next group of similar column details for the user to decide on.
        Will return same group until decision is made.
        """
        if self.current_similar_columns:
            return self.current_similar_columns

        self.current_similar_columns = self._similarity_matches.pop()
        return self.current_similar_columns

    def remaining_count(self) -> int:
        """
        Get # of remaining similar column groups to check
        """
        return len(self._similarity_matches)

    def merge_columns(self, final_col: pd.Series):
        """
        Select to merge the columns found in self.current_similar_columns

        Parameters
        ----------
        final_col : pd.Series
            The final column series from the user editable dataframe
        """
        columns_to_remove = self.current_similar_columns.perform_merge(final_col)
        self.columns_to_remove = self.columns_to_remove.union(columns_to_remove)

        self.current_similar_columns = None
        st.experimental_rerun()

    def dont_merge_columns(self):
        """
        Decide not to merge the similar column group find in self.current_similar_columns
        """
        self.current_similar_columns = None
        st.experimental_rerun()
