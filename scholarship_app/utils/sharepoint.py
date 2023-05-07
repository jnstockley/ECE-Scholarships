"""
Sharepoint Handler
Gets cookie manager
Ensure login
Uploads files
Downloads files
"""
import os.path
import re
import time
from os.path import exists
from re import Pattern

import extra_streamlit_components as stx
from extra_streamlit_components import CookieManager
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext
from streamlit.errors import DuplicateWidgetID

VALID_EXTENSIONS = (".xls", ".xlsx", ".csv")

HAWKID_REGEX = re.compile(r"[a-zA-Z][a-zA-Z0-9]{2,}@uiowa.edu")

PASSWORD_REGEX = re.compile(
    r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&]?)[A-Za-z\d@$!%*#?&]{8,}$"
)

SITE_URL_REGEX = re.compile(r"https://iowa.sharepoint.com/sites/.+")


def get_manager():
    """
    Cookie Manager    :return: , to access login creds
    """
    return stx.CookieManager(key="cookie-manager")


def regex_validation(string: str, regex: Pattern[str]) -> bool | None:
    """
    Validates regex, used to check sign in creds before connecting to sharepoint
    :param string: String to match
    :param regex: Regex used to match against the string
    :return: True if matches, otherwise none
    """
    return re.fullmatch(regex, string)


def logged_in(
    manager: CookieManager = None, creds: dict = None
) -> bool | CookieManager:
    """
    Checks if the cookies are present, and in a valid format
    :param manager: Optional cookie manager, use if used more than once per page
    :param creds: Sharepoint login connection
    :return: True if logged in, False otherwise, CookieManager only for internal user
    """
    if manager is None:
        manager = get_manager()

    # Work around for caching not working with cookie manager
    time.sleep(0.2)

    if creds is None:
        cookies = {}
        # Work around for `duplicate` cookie managers
        try:
            cookies = manager.get_all()
        except DuplicateWidgetID:
            pass
        # Work around for caching not working with cookie manager
        if cookies == {}:
            return logged_in(manager)
        if "cred" not in cookies:
            return False
        creds = manager.get("cred")
    if (
        isinstance(creds, dict)
        and "hawk-id" not in creds
        and "password" not in creds
        and "site-url" not in creds
    ):
        return False
    hawk_id = creds["hawk-id"]
    password = creds["password"]
    site_url = creds["site-url"]
    if (
        regex_validation(hawk_id, HAWKID_REGEX)
        and regex_validation(password, PASSWORD_REGEX)
        and regex_validation(site_url, SITE_URL_REGEX)
    ):
        return manager
    return False


def login(manager: CookieManager = None) -> ClientContext | None:
    """
    Makes the first connection to sharepoint and ensure the connection was successful
    :param manager: Optional cookie manager, use if used more than once per page
    :return: Sharepoint connection if successful, otherwise None
    """
    if manager is None:
        manager = get_manager()

    creds = manager.get("cred")

    hawk_id = creds["hawk-id"]
    password = creds["password"]
    site_url = creds["site-url"]

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

    data = ["Select File"] + [
        str(f.properties["ServerRelativeUrl"]).split(target_folder_url)[1]
        for f in files
        if str(f.properties["ServerRelativeUrl"]).endswith(VALID_EXTENSIONS)
    ]

    return data


def download(file: str, download_location: str, cred: ClientContext) -> bool:
    """
    Downloads a specified file from Sharepoint
    :param file: Sharepoint file path
    :param download_location: Location, on disk, to download the file
    :param cred: Sharepoint login connection
    :return: True if file downloaded successfully, False otherwise
    """
    full_site_url: str = f"{cred.web.url}/"
    site_url = full_site_url.split(".com")[1]
    root_folder = "Shared Documents"
    download_url = f"{site_url}{root_folder}{file}"
    file_name = file.split("/")[len(file.split("/")) - 1]
    if not download_location.endswith("/"):
        download_location += "/"
    with open(f"{download_location}{file_name}", "wb") as sharepoint_file:
        cred.web.get_file_by_server_relative_url(download_url).download(
            sharepoint_file
        ).execute_query()
    return exists(f"{download_location}{file_name}")


def upload(full_file_path: str, upload_location: str, cred: ClientContext) -> bool:
    """
    Uploads a file to sharepoint
    :param full_file_path: Full path to the location of the file on disk
    :param upload_location: Location for where to upload the file to Sharepoint
    :param cred: Sharepoint login connection
    :return: True if the file is uploaded successfully, False otherwise
    """
    if not exists(full_file_path):
        return False

    full_site_url: str = f"{cred.web.url}/"
    site_url = full_site_url.split(".com")[1]
    root_folder = "Shared Documents"
    upload_url = f"{site_url}{root_folder}{upload_location}"

    folder = cred.web.get_folder_by_server_relative_url(upload_url)

    print(f"{upload_url}/{os.path.basename(full_file_path)}")

    with open(full_file_path, "rb") as file:
        file = folder.files.create_upload_session(file, 1000000).execute_query()

    return f"{upload_url}/{os.path.basename(full_file_path)}" == file.serverRelativeUrl
