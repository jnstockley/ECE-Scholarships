"""
Objects for importing the sharepoint user session and interfacing with sharepoint.
"""
from enum import Enum
import json
import os
import time
import extra_streamlit_components as stx
from streamlit.runtime.state import SessionStateProxy
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from scholarship_app.managers.config import ConfigManager
from scholarship_app.utils.html import redirect
from scholarship_app.sessions.session_manager import SessionManager
from scholarship_app.utils.output import get_appdata_path

COOKIE_CREDENTIALS_KEY = "sharepoint-auth"
VALID_EXTENSIONS = (".xls", ".xlsx", ".csv")
SHAREPOINT_CONFIG_KEY = "sharepoint_url"

def get_cookie_manager():
    """
    Returns (and attempts to cache) cookie manage object
    """
    return stx.CookieManager("sharepoint-cookies")


class Session(Enum):
    """
    sharepoint session keys
    """
    CREDENTIALS = "creds"
    REDIRECT_AFTER_SYNC = "redirect"
    SHAREPOINT_URL = "sharepoint_url"


class SharepointSession(SessionManager):
    """
    This class handles statefullness of the streamlit session. If a user is signed in, etc.

    Attributes
    ----------
    client : ClientContent | None
        Main sharepoint client config reference
    sharepoint_url : str
        Sharepoint configured URL (with no trailing /)
    verified : bool
        Whether the client has already been verified with sharepoint
    sync_complete : bool
        Whether the session/cookie sync has been completed
    _cookie_manager : CookieManager
        Returns cookie manager object from streamlit extras
    """

    def __init__(self, session: SessionStateProxy):
        super().__init__(session, "auth", "default")

        if self.has(Session.SHAREPOINT_URL):
            self.sharepoint_url = self.retrieve(Session.SHAREPOINT_URL)
        else:
            self.sharepoint_url = self.retrieve_sharepoint_url()
            self.set(Session.SHAREPOINT_URL, self.sharepoint_url)

        self._cookie_manager = get_cookie_manager()
        self.verified = False
        self.hawk_id = None

        # This manages saving session date to cookie and cookie to session date
        # Cookie manipulation can only be done at streamlit session start which is why it is
        # called on init. Since form submit reinitializes script, this will get called on login.
        self._sync_session()

        self.client = None
        if self.has(Session.CREDENTIALS):
            hawk_id, password = self._retrieve_credentials()
            self._login_no_verify(hawk_id, password)

    def retrieve_sharepoint_url(self) -> str | None:
        '''
        Gets the sharepoint URL
        '''
        config = ConfigManager()
        if config.has_key(SHAREPOINT_CONFIG_KEY):
            return config.data[SHAREPOINT_CONFIG_KEY]

        return None

    def get_hawk_id(self) -> str | None:
        """
        Returns hawk ID if one is defined
        """
        return self.hawk_id

    def is_signed_in(self) -> bool:
        """
        Returns if user is signed in

        Returns
        -------
            True if user signed in to sharepoint
        """
        self._wait_for_sync_complete()
        return self.client is not None

    def logout(self):
        """
        Log the user out of the current session and remove cookie
        """
        self._unset(Session.CREDENTIALS)
        self._cookie_manager.delete(COOKIE_CREDENTIALS_KEY)
        time.sleep(0.5)

    def login(self, hawk_id: str, password: str) -> bool:
        """
        Attempts to login the ClientContext for sharepoint user credentials

        Returns
        -------
            True for success, false for failure.
        """
        self.client = ClientContext(self.sharepoint_url.strip("/")).with_credentials(
            UserCredential(hawk_id, password)
        )

        # Verify the client was properly configured with test request
        try:
            result = self._verify()
        except:
            self.client = None
            return False

        if result:
            self.hawk_id = hawk_id
            self.set(Session.CREDENTIALS, {"username": hawk_id, "password": password})
            return True

        self.client = None
        return False

    def get_files(self) -> list[str]:
        """
        Gets a list of files on the sharepoint site

        Returns
        -------
        List of files stored in sharepoint
        """
        target_folder_url = "Shared Documents"

        root_folder = self.client.web.get_folder_by_server_relative_path(
            target_folder_url
        )

        files = root_folder.get_files(True).execute_query()

        data = ["Select File"] + [
            str(f.properties["ServerRelativeUrl"]).split(target_folder_url)[1]
            for f in files
            if str(f.properties["ServerRelativeUrl"]).endswith(VALID_EXTENSIONS)
        ]

        return data

    def upload(self, appdata_path: str, upload_location: str):
        """
        Uploads a file to sharepoint

        Inputs
        ------
        appdata_path
            Full path to the location of the file inside appdata
        upload_location
            Location for where to upload the file to Sharepoint

        Returns
        -------
            True if the file is uploaded successfully, False otherwise
        """
        local_file_path = get_appdata_path(appdata_path)

        if not os.path.exists(local_file_path):
            return False

        self._verify()

        full_site_url: str = f"{self.client.web.url}/"
        site_url = full_site_url.split(".com")[1]
        root_folder = "Shared Documents/"
        upload_url = f"{site_url}{root_folder}{upload_location}"

        folder = self.client.web.get_folder_by_server_relative_url(upload_url)

        with open(local_file_path, "rb") as file:
            file = folder.files.create_upload_session(file, 1000000).execute_query()

        return (
            f"{upload_url}/{os.path.basename(local_file_path)}"
            == file.serverRelativeUrl
        )

    def download(self, sharepoint_path: str, appdata_path: str) -> bool:
        """
        Downloads a specified file from Sharepoint

        Inputs
        ------
        sharepoint_path
            Full path to the location of the file inside appdata
        appdata_path
            Location, on disk, to download the file

        Returns
        -------
            True if file downloaded successfully, False otherwise
        """
        self._verify()

        full_appdata_path = get_appdata_path(appdata_path)

        full_site_url: str = f"{self.client.web.url}/"
        site_url = full_site_url.split(".com")[1]
        root_folder = "Shared Documents"
        download_url = f"{site_url}{root_folder}{sharepoint_path}"
        file_name = sharepoint_path.split("/")[len(sharepoint_path.split("/")) - 1]

        if not full_appdata_path.endswith("/"):
            full_appdata_path += "/"
        with open(f"{full_appdata_path}{file_name}", "wb") as sharepoint_file:
            self.client.web.get_file_by_server_relative_url(download_url).download(
                sharepoint_file
            ).execute_query()
        if not os.path.exists(full_appdata_path):
            os.mkdir(full_appdata_path)
        return os.path.exists(f"{full_appdata_path}{file_name}")

    def set_redirect(self, url: str):
        """
        Redirecting before cookie sync will cause cookie to not be saved. When using sharepoint session
        to redirect correctly use set_redirect(), which will redirect on next page re-render
        """
        self.set(Session.REDIRECT_AFTER_SYNC, url)

    def _handle_redirect(self):
        """
        If Session.REDIRECT_AFTER_SYNC has value, redirect to it
        """
        if self.has(Session.REDIRECT_AFTER_SYNC):
            redirect_to = self.retrieve(Session.REDIRECT_AFTER_SYNC)
            self._unset(Session.REDIRECT_AFTER_SYNC)
            redirect(redirect_to)

    def _verify(self) -> bool:
        """
        Verifies client and retrieves data. This must be called before any upload/download
        request can be performed. Will throw error if failed

        Returns
        -------
        bool
            Whether the verification succeeded.
        """
        if self.verified:
            return True

        if self.client is None:
            return False

        web = self.client.web.get().execute_query()

        if not f"{web.url}/".strip("/") == self.sharepoint_url.strip("/"):
            return False

        self.verified = True
        return True

    def _sync_session(self):
        """
        Sync session and cookie
        """
        if self.has(Session.CREDENTIALS):
            # Cookie needs to be synced with session, presume session is known truth
            json_str = json.dumps(self.retrieve(Session.CREDENTIALS), indent=4)
            self._cookie_manager.set(COOKIE_CREDENTIALS_KEY, json_str)

            self._wait_for_cookie_key(COOKIE_CREDENTIALS_KEY, max_wait=5)

            # If queued redirect waiting, we can now redirect
            self._handle_redirect()
            self.sync_complete = True
            return

        if COOKIE_CREDENTIALS_KEY in self._cookie_manager.get_all():
            cookie_value = self._cookie_manager.get(COOKIE_CREDENTIALS_KEY)
            self.set(Session.CREDENTIALS, cookie_value)

        self._handle_redirect()
        self.sync_complete = True

    def _login_no_verify(self, hawk_id: str, password: str):
        """
        Same behavior as login but assumes hawk_id and password are already valid.
        This also does not modify cookie or session.
        """
        self.client = ClientContext(self.sharepoint_url).with_credentials(
            UserCredential(hawk_id, password)
        )

        self.hawk_id = hawk_id
        self.set("sharepoint_auth", {"username": hawk_id, "password": password})

    def _retrieve_credentials(self):
        """
        Retrieves the session or cookie credentials

        Returns
        -------
        hawkid, password
        """
        creds = self.retrieve(Session.CREDENTIALS)
        return creds["username"], creds["password"]

    def _wait_for_cookie_key(self, key: str, max_wait: float = 1):
        """
        Waits until the key is present in the cookie or until max_wait, whichever first.
        """
        sleep = 0.1
        wait_time = 0
        while key not in self._cookie_manager.get_all() or wait_time > max_wait:
            time.sleep(sleep)
            wait_time += sleep

    def _wait_for_sync_complete(self, max_wait=0.5):
        """
        Waits until client found or max_wait seconds have passed
        """
        sleep = 0.01
        elapsed = 0
        while not self.client and elapsed < max_wait:
            time.sleep(0.01)
            elapsed += sleep
