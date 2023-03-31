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


def get_files() -> list[str]:
    """
    Gets a list of files on the sharepoint site
    :return: List of files stored in sharepoint
    """
    return []


def download():
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
