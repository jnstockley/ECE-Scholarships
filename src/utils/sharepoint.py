"""
Sharepoint Handler
Gets cookie manager
Ensure login
Uploads files
Downloads files
"""

import extra_streamlit_components as stx


def get_manager():
    """
    Cookie Manager    :return: , to access login creds
    """
    return stx.CookieManager()


def logged_in() -> bool:
    """
    Checks if the cookies are present, and in a valid format
    :return: True if cookie looks good, otherwise false
    """
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
