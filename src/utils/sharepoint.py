"""
Sharepoint Handler
Gets cookie manager
Ensure login
Uploads files
Downloads files
"""
import re
import time
from re import Pattern

import extra_streamlit_components as stx
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext

VALID_EXTENSIONS = (".xls", ".xlsx", ".csv")

HAWKID_REGEX = re.compile(r"[a-zA-Z]{1}[a-zA-Z0-9]{2,}@uiowa.edu")

PASSWORD_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&]?)[A-Za-z\d@$!%*#?&]{8,}$")

SITE_URL_REGEX = re.compile(r"https://iowa.sharepoint.com/sites/.+")


def get_manager():
    """
    Cookie Manager    :return: , to access login creds
    """
    return stx.CookieManager()


def regex_validation(string: str, regex: Pattern[str]) -> bool | None:
    """
    Validates regex, used to check sign in creds before connecting to sharepoint
    :param string: String to match
    :param regex: Regex used to match against the string
    :return: True if matches, otherwise none
    """
    return re.fullmatch(regex, string)


def logged_in() -> bool:
    """
    Checks if the cookies are present, and in a valid format
    :return: True if cookie looks good, otherwise false
    """
    # Work around for caching not working with cookie manager
    time.sleep(0.2)

    manager = get_manager()
    cookies = manager.get_all()
    if "cred" not in cookies:
        return False
    creds = manager.get("cred")
    if type(creds) is dict and "hawk-id" not in creds and "password" not in creds and "site-url" not in creds:
        return False
    hawk_id = creds['hawk-id']
    password = creds['password']
    site_url = creds['site-url']
    if regex_validation(hawk_id, HAWKID_REGEX) and regex_validation(password, PASSWORD_REGEX) \
            and regex_validation(site_url, SITE_URL_REGEX):
        return True
    return False


def login() -> ClientContext | None:
    """
        Makes the first connection to sharepoint and ensure the connection was successful
        :param hawk_id: Username
        :param password: Password
        :param site_url: Sharepoint Site URL
        :return: O365 Creds object, False None otherwise
        """

    if not logged_in():
        return None

    creds = get_manager().get("cred")

    hawk_id = creds['hawk-id']
    password = creds['password']
    site_url = creds['site-url']

    creds = ClientContext(site_url).with_credentials(UserCredential(hawk_id, password))
    try:
        web = creds.web.get().execute_query()
    except IndexError:
        return None
    except ClientRequestException:
        return None
    if f"{web.url}/" == site_url:
        return creds
    return None


def get_files(creds: ClientContext) -> list[str]:
    """
    Gets a list of files on the sharepoint site
    :return: List of files stored in sharepoint
    """
    target_folder_url = "Shared Documents"

    root_folder = creds.web.get_folder_by_server_relative_path(target_folder_url)

    files = root_folder.get_files(True).execute_query()

    data = ["Select File"] + [str(f.properties['ServerRelativeUrl']).split(target_folder_url)[1] for f in files if
                              str(f.properties['ServerRelativeUrl']).endswith(VALID_EXTENSIONS)]

    return data


def download(file: str):
    """
    Downloads a specified file from sharepoint
    """
    return None


def upload() -> bool:
    """
    Uploads a file to sharepoint
    :return: True if the file was uploaded, otherwise False
    """
    return False
