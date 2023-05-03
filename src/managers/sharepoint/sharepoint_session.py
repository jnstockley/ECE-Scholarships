'''
Objects for importing the sharepoint user session and interfacing with sharepoint.
'''
from enum import Enum
from streamlit.runtime.state import SessionStateProxy
from src.sessions.session_manager import SessionManager
from office365.runtime.client_request_exception import ClientRequestException
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
        Main sharepoint client config reference
    sharepoint_url : str
        Sharepoint configured URL (with no trailing /)
    '''
    def __init__(self, session: SessionStateProxy):
        super().__init__(session, "default")

        self.sharepoint_url = SHAREPOINT_URL.strip("/")

        self.client = None
        if self.has(Session.CREDENTIALS):
            hawk_id, password = self._retrieve_credentials()
            self._login_no_verify(hawk_id, password)

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

        # Verify the client was properly configured with test request
        try:
            web = self.client.web.get().execute_query()
        except IndexError:
            return False
        except ClientRequestException:
            return False

        if f"{web.url}/".strip("/") == self.sharepoint_url:
            return True

        return False

    def _login_no_verify(self, hawk_id: str, password: str):
        '''
        Same behavior as login but assumes hawk_id and password are already valid.
        '''
        self.client = ClientContext(SHAREPOINT_URL).with_credentials(UserCredential(hawk_id, password))

        self._set(Session.CREDENTIALS, {"username": hawk_id, "password": password})

    def _retrieve_credentials(self):
        '''
        Retrieves the session or cookie credentials

        Returns
        -------
        hawkid, password
        '''
        creds = self._retrieve(Session.CREDENTIALS)
        return creds["username"], creds["password"]
