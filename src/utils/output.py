'''
Output I/O interfaces for runtime
'''
import os

APP_DATA = ".app_data"

def create_directory(path: str) -> None:
    '''
    Creates path if it doesn't exist
    '''
    if not os.path.exists(path):
        os.makedirs(path)

def get_appdata_path(appdata_path: str = "") -> str:
    '''
    Returns the output data directory for runtime. Will create the directory
    if it is not already present.

    Parameters
    ----------
    appdata_path : str, optional
        Path of file in appdata
    '''
    print("RECEIVED PATH:")
    print(appdata_path)
    path = os.path.join(APP_DATA, appdata_path.strip("/"))
    print(path)

    create_directory(path)

    return path
