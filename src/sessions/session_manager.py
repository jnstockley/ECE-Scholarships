'''
SessionManager
'''
from enum import Enum
import streamlit as st
from streamlit.runtime.state import SessionStateProxy

class GlobalSession(Enum):
    '''
    Global shared sessions
    '''
    VIEW = "view"

class SessionManager:
    '''
    Main session manager object for simplifying streamlit session logic in views.
    '''
    def __init__(self, session: SessionStateProxy, default_view):
        self._session = session

        if not self.has(GlobalSession.VIEW):
            self._set(GlobalSession.VIEW, default_view)

        self.view = self._retrieve(GlobalSession.VIEW)

    def set_view(self, view):
        '''
        Sets current page view
        '''
        self._set(GlobalSession.VIEW, view)
        st.experimental_rerun()

    def has(self, key: str):
        '''
        Verifies key is present in current session.
        '''
        return key in self._session

    def _retrieve(self, key: str):
        '''
        Checks whether the st.session contains key. If not throws error
        '''
        if self.has(key) and self._session[key] is not None:
            return self._session[key]

        raise KeyError(f'Key "{key}" not found in session')

    def _set(self, key: str, value):
        '''
        Sets session state key value.
        '''
        if self.has(key):
            cur_type = type(self._retrieve(key))
            new_type = type(value)
            if cur_type is not new_type:
                raise TypeError(f'Trying to set session_key={key} of type {cur_type} to invalid type {new_type}\nSession state types shall not deviate!')

        self._session[key] = value
