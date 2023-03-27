'''
Output I/O interfaces for runtime
'''
import os

APP_DATA = ".app_data"

def get_output_dir():
    '''
    Returns the output data directory for runtime. Will create the directory
    if it is not already present.
    '''
    if not os.path.exists(APP_DATA):
        os.makedirs(APP_DATA)

    return APP_DATA
