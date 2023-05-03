'''
Managers for handling .appdata directory
'''
import os

APP_DATA = ".app_data"

class AppDataManager:
    '''
    Manages files in the app data directory
    '''
    def __init__(self):
        if not os.path.exists(APP_DATA):
            os.makedirs(APP_DATA)
