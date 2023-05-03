'''
Objects for importing the sharepoint user session and interfacing with sharepoint.
'''
from enum import Enum
from streamlit.runtime.state import SessionStateProxy
from src.sessions.session_manager import SessionManager
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

#TODO: Temporary
SHAREPOINT_URL = "https://iowa.sharepoint.com/sites/SEP2023-Team2/"

class Session(Enum):
    '''
    sharepoint session keys
    '''
    CREDENTIALS = "creds"

class SharepointSession(SessionManager):
    '''
    This class handles statefullness of the streamlit session. If a user is signed in, etc.

    Attributes
    ----------
    client : ClientContent | None
    '''
    def __init__(self, session: SessionStateProxy):
        super().__init__(session, "default")

        self.client = None
        if self.has(Session.CREDENTIALS):
            hawk_id, password = self._retrieve_credentials()
            self.login(hawk_id, password)

    def is_signed_in(self) -> bool:
        '''
        Returns if user is signed in

        Returns
        -------
            True if user signed in to sharepoint
        '''
        return self.client is not None

    def login(self, hawk_id: str, password: str) -> bool:
        '''
        Attempts to login the ClientContext for sharepoint user credentials

        Returns
        -------
            True for success, false for failure.
        '''
        self.client = ClientContext(SHAREPOINT_URL).with_credentials(UserCredential(hawk_id, password))

        self._set(Session.CREDENTIALS, {"username": hawk_id, "password": password})
        return True

    def _retrieve_credentials(self):
        '''
        Retrieves the session or cookie credentials

        Returns
        -------
        hawkid, password
        '''
        creds = self._retrieve(Session.CREDENTIALS)
        return creds["username"], creds["password"]
