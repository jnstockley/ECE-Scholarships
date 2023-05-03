'''
SessionManager
'''
from enum import Enum
import time
import streamlit as st
import pandas as pd
from streamlit.runtime.state import SessionStateProxy

class GlobalSession(Enum):
    '''
    Global shared sessions
    '''
    VIEW = "view"
    DATA_MAIN = "data_main"

class SessionManager:
    '''
    Main session manager object for simplifying streamlit session logic in views.
    
    Attributes
    ----------
    data : pd.DataFrame
        The main student dataframe set by import logic
    view : any
        Current view for pages session
    '''
    def __init__(self, session: SessionStateProxy, default_view):
        self._session = session

        if not self.has(GlobalSession.VIEW):
            self.set(GlobalSession.VIEW, default_view)
            self.view = default_view
        else:
            self.view = self.retrieve(GlobalSession.VIEW)

        if self.has(GlobalSession.DATA_MAIN):
            self.data = self.retrieve(GlobalSession.DATA_MAIN)

    def set_view(self, view):
        '''
        Sets current page view
        '''
        self.set(GlobalSession.VIEW, view)
        st.experimental_rerun()

    def get_view(self):
        '''
        Get the current view
        '''
        return self.view

    def has(self, key: str):
        '''
        Verifies key is present in current session.
        '''
        return key in self._session and self._session[key] is not None

    def set_main_data_source(self, data: pd.DataFrame):
        '''
        Sets the main scholarship dataframe for the user session
        '''
        self.set(GlobalSession.DATA_MAIN, data)

    def retrieve(self, key: str):
        '''
        Checks whether the st.session contains key. If not throws error
        '''
        if self.has(key):
            return self._session[key]

        raise KeyError(f'Key "{key}" not found in session')

    def set(self, key: str, value):
        '''
        Sets session state key value.
        '''
        if self.has(key):
            cur_type = type(self.retrieve(key))
            new_type = type(value)
            if cur_type is not new_type:
                raise TypeError(f'Trying to set session_key={key} of type {cur_type} to invalid type {new_type}\nSession state types shall not deviate!')

        self._session[key] = value

    def _unset(self, key: str):
        '''
        Unsets a session value
        '''
        if self.has(key):
            del self._session[key]
