from streamlit.runtime.state import SessionStateProxy

class SessionManager:
    def __init__(self, session: SessionStateProxy):
        self._session = session

    def _has(self, key: str):
        '''
        Verifies key is present in current session.
        '''
        return key in self._session

    def _retrieve(self, key: str):
        '''
        Checks whether the st.session contains key. If not throws error
        '''
        if self._has(key) and self._session[key] is not None:
            return self._session[key]
        
        raise KeyError(f'Key "{key}" not found in session')

    def _set(self, key: str, value):
        '''
        Sets session state key value.
        '''
        if self._has(key):
            cur_type = type(self._retrieve(key))
            new_type = type(value)
            if cur_type is not new_type:
                raise TypeError(f'Trying to set session_key={key} of type {cur_type} to invalid type {new_type}\nSession state types shall not deviate!')

        self._session[key] = value