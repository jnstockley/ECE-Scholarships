'''
Output I/O interfaces for runtime
'''
import os

APP_DATA = ".app_data"

def get_output_dir(sub_dir: str = "") -> str:
    '''
    Returns the output data directory for runtime. Will create the directory
    if it is not already present.

    Parameters
    ----------
    sub_dir : str, optional
        Subdirectory output file will be written to, will create if not present
    '''
    path = os.path.join(APP_DATA, sub_dir)

    if not os.path.exists(path):
        os.makedirs(path)

    return path
