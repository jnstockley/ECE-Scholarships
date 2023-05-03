'''
Objects for importing the sharepoint user session and interfacing with sharepoint.
'''
from enum import Enum
import json
import extra_streamlit_components as stx
from streamlit.runtime.state import SessionStateProxy
from office365.runtime.client_request_exception import ClientRequestException
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from src.sessions.session_manager import SessionManager

# temporary:
SHAREPOINT_URL = "https://iowa.sharepoint.com/sites/SEP2023-Team2/"
COOKIE_CREDENTIALS_KEY = "sharepoint-auth"

def get_cookie_manager():
    '''
    Returns (and attempts to cache) cookie manage object
    '''
    return stx.CookieManager("sharepoint-cookies")

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
    _cookie_manager : CookieManager
        Returns cookie manager object from streamlit extras
    '''
    def __init__(self, session: SessionStateProxy):
        super().__init__(session, "default")

        self._cookie_manager = get_cookie_manager()

        # This manages saving session date to cookie and cookie to session date
        # Cookie manipulation can only be done at streamlit session start which is why it is
        # called on init. Since form submit reinitializes script, this will get called on login.
        self._sync_session()

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
        client = ClientContext(SHAREPOINT_URL).with_credentials(UserCredential(hawk_id, password))

        # Verify the client was properly configured with test request
        try:
            web = client.web.get().execute_query()
        except IndexError:
            return False
        except ClientRequestException:
            return False

        if f"{web.url}/".strip("/") == self.sharepoint_url:
            self._set(Session.CREDENTIALS, {"username": hawk_id, "password": password})
            self.client = client
            return True

        return False

    def _sync_session(self):
        '''
        Sync session and cookie
        '''
        if self.has(Session.CREDENTIALS):
            # Cookie needs to be synced with session, presume session is known truth
            json_str = json.dumps(self._retrieve(Session.CREDENTIALS), indent = 4)
            self._cookie_manager.set(COOKIE_CREDENTIALS_KEY, json_str)

            return

        if COOKIE_CREDENTIALS_KEY in self._cookie_manager.get_all():
            print("Found cookie but not session")
            cookie_value = self._cookie_manager.get(COOKIE_CREDENTIALS_KEY)
            self._set(Session.CREDENTIALS, cookie_value)

    def _login_no_verify(self, hawk_id: str, password: str):
        '''
        Same behavior as login but assumes hawk_id and password are already valid.
        This also does not modify cookie or session.
        '''
        self.client = ClientContext(SHAREPOINT_URL).with_credentials(UserCredential(hawk_id, password))

        self._set("sharepoint_auth", {"username": hawk_id, "password": password})

    def _retrieve_credentials(self):
        '''
        Retrieves the session or cookie credentials

        Returns
        -------
        hawkid, password
        '''
        creds = self._retrieve(Session.CREDENTIALS)
        return creds["username"], creds["password"]
