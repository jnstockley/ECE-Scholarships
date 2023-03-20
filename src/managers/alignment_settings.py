
import pandas as pd
import src.utils.merge as merge
from src.models.imported_sheet import ImportedSheet

class SelectAlignment:
    def __init__(self, column: str, sheet: ImportedSheet):
        self.column = column
        self.sheet = sheet

    def get_alignment_col(self):
        return self.sheet.get_df()[self.column]

class AlignmentInfo:
    def __init__(self, drop_missing: bool, final_column_name: str, selected_alignment_columns: list[SelectAlignment]):
        self.drop_missing = drop_missing
        self.final_column_name = final_column_name
        self.selected_alignment_columns = selected_alignment_columns

        self.combine_columns = [setting.get_alignment_col() for setting in selected_alignment_columns]
        self.final_alignment_column = merge.combine_columns(self.combine_columns, self.drop_missing)
