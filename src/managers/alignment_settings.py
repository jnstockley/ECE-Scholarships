'''
General objects for the alignment column UI logic.
'''
import dataclasses
import pandas as pd
from src.utils import merge
from src.models.imported_sheet import ImportedSheet

class SelectAlignment:
    '''
    Defines what column is selected as the alignment column for an imported sheet
    '''
    def __init__(self, column: str, sheet: ImportedSheet):
        self.column = column
        self.sheet = sheet

    def get_alignment_col(self) -> pd.Series:
        '''
        Returns the pandas series reference of the alignment column in question
        '''
        return self.sheet.get_df()[self.column]

    def get_column(self) -> str:
        '''
        Return alignment column name for dataset
        '''
        return self.column

class DuplicateColumnData:
    '''
    Stores information about a duplicate value that differs between duplicate columns found between
    multiple datasets

    Attributes
    ----------
    alignment_row_value : any
        The value found in the alignment column's row (unique value for identifying the row of the dataset)
    duplicate_column_name : str
        Name of the duplicate column these values are kept in
    affected_alignment_data : list[SelectedAlignment]
        The referenced selected alignment dataset objects for reference.
    '''
    def __init__(self, alignment_row_value: str, duplicate_column_name: str, affected_alignment_data: list[SelectAlignment]):
        self.alignment_row_value = alignment_row_value
        self.duplicate_column_name = duplicate_column_name
        self.affected_alignment_data = affected_alignment_data

    def get_values(self) -> set[any]:
        '''
        Returns all the unique values in this duplicate column row from each of the imported dataframes.
        '''
        values = []

        for alignment_data in self.affected_alignment_data:
            data = alignment_data.sheet.get_df()
            values.append(data.loc[data[alignment_data.column] == self.alignment_row_value, self.duplicate_column_name].tolist()[0])

        return set(values)

    def get_comparison_df(self) -> pd.DataFrame:
        '''
        Returns a dataframe with column name being the name of the import file and value being
        the value the duplicate column name is inside that associated dataset.
        '''
        return pd.DataFrame()

    def override_value(self, value):
        '''
        Sets the value of all of the duplicate columns in each dataframe to this value
        '''

@dataclasses.dataclass
class AlignmentInfo:
    '''
    drop_missing : bool
        Whether index data not present in all dataframes should be kept or dropped from final output
    final_column_name : str
        Final alignment column name in output df.
    selected_alignment_columns : list[SelectAlignment]
        List of all the selected alignment objects.
    '''
    drop_missing: bool
    final_column_name: str
    selected_alignment_columns: list[SelectAlignment]


class AlignmentManager:
    '''
    Class for maintaing state of the alignment column alignment process

    Attributes
    ----------
    info : AlignmentInfo
        Info the user selected regarding the alignment data
    drop_missing : bool
        Whether index data not present in all dataframes should be kept or dropped from final output
    final_column_name : str
        Final alignment column name in output df.
    selected_alignment_columns : list[SelectAlignment]
        List of all the selected alignment objects.
    current_align_index : int
        Current index that needs alignment
    max_align_index : int
        Maximum index to align, if drop_missing, it equals the max index of the minimum length dataframe.
        Otherwise it will equal max index of the largest dataframe.
    combine_columns : list[pd.Series]
        List of all the alignment columns to merge.
    final_alignment_column : pd.Series
        Final aligned column in its current alignment state.
    duplicate_df_columns : set[str]
        Set of the duplicate columns found between the alignment dataframes
    '''
    def __init__(self, drop_missing: bool, final_column_name: str, selected_alignment_columns: list[SelectAlignment]):
        self.info = AlignmentInfo(drop_missing, final_column_name, selected_alignment_columns)

        self.combine_columns = [setting.get_alignment_col() for setting in selected_alignment_columns]
        self.final_alignment_column = merge.combine_columns(self.combine_columns, self.info.drop_missing)

        self._duplicate_df_columns = self._find_duplicate_columns()
        self._mismatched_duplicate_column_row = self._find_duplicate_columns_with_differing_data()
        print(f"Total mismatches = {len(self._mismatched_duplicate_column_row)}")

        # find mismatched columns
    def pop_next_duplicate_to_handle(self):
        '''
        Returns next duplicate to handle from the 
        '''
        return self._mismatched_duplicate_column_row.pop()

    def alignment_complete(self) -> bool:
        '''
        Returns whether user has went through all duplicate columns that differ in values.
        '''
        return len(self._mismatched_duplicate_column_row) == 0

    def _find_duplicate_columns(self) -> set[str]:
        '''
        Returns duplicate columns found in each of the input dataframes
        '''
        alignment_columns: list[str] = []
        columns: list[set[str]] = []

        for selected_alignment in self.info.selected_alignment_columns:
            alignment_columns.append(selected_alignment.column)
            data = selected_alignment.sheet.get_df()
            columns.append(set(data.columns.tolist()))

        return {column for column in set.intersection(*columns) if column not in alignment_columns}

    def _find_duplicate_columns_with_differing_data(self) -> list[DuplicateColumnData]:
        '''
        From the list of duplicate columns, will find any rows based on unique alignment column value with duplicate column
        that differs between the set of input dataframes.
        '''
        mismatches = []

        for _index, value in self.final_alignment_column.items():
            affected_alignment_data: list[SelectAlignment] = []
            for duplicate_column in self._duplicate_df_columns:
                affected_alignment_data: list[SelectAlignment] = []

                # step 1: aquire relevant dataframes (all dataframes with duplicate column and index value)
                for selected_alignment in self.info.selected_alignment_columns:
                    data = selected_alignment.sheet.get_df()
                    if duplicate_column in data.columns.tolist() and value in data[selected_alignment.column].tolist():
                        affected_alignment_data.append(selected_alignment)


                prev_val = None
                for data in affected_alignment_data:
                    cur_val = data.sheet.get_df().loc[data.sheet.get_df()[data.column] == value, duplicate_column].tolist()[0]

                    if prev_val is None:
                        prev_val = cur_val
                    elif not prev_val == cur_val:
                        #mismatch detected. Needs to be handled:
                        mismatches.append(DuplicateColumnData(value, duplicate_column, affected_alignment_data))
                        break

        return mismatches
