'''
Imported data sheet representation
'''
import os
import pandas as pd

class ImportedSheet:
    '''
    Object represenation of 
    '''
    def __init__(self, path):
        '''
        Initialize an object given a path.
        '''
        self._path = path
        self._file_name = os.path.basename(path)
        self._data = None

    def get_file_name(self):
        '''
        Getter for file path basename
        '''
        return self._file_name

    def get_df(self):
        '''
        Gets the pandas dataframe
        '''
        if self._data is None:
            self._load_file_into_memory()

        return self._data

    def get_path(self):
        '''
        Getter for file path
        '''
        return self._path

    def _load_file_into_memory(self):
        '''
        Takes the file path and loads it into memory
        Will handle whether file is csv or excel.
        '''
        self._data = pd.read_excel(self._path)
