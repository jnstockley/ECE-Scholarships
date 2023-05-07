"""
Imported data sheet representation
"""
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile


class ImportedSheet:
    """
    Object represenation of
    """

    def __init__(self, file: UploadedFile):
        """
        Initialize an object given a path.
        """
        self._file = file
        self._data = None

        self.file_name = file.name

    def get_df(self):
        """
        Gets the pandas dataframe
        """
        if self._data is None:
            self.load_file_into_memory()

        return self._data

    def load_file_into_memory(self):
        """
        Takes the file path and loads it into memory
        Will handle whether file is csv or excel.
        """
        self._data = pd.read_excel(self._file)
