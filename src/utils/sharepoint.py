"""
Sharepoint Handler
Gets cookie manager
Ensure login
Uploads files
Downloads files
"""
import os.path
import re
from os.path import exists
from re import Pattern

from office365.sharepoint.client_context import ClientContext

VALID_EXTENSIONS = (".xls", ".xlsx", ".csv")

HAWKID_REGEX = re.compile(r"[a-zA-Z][a-zA-Z0-9]{2,}@uiowa.edu")
PASSWORD_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&]?)[A-Za-z\d@$!%*#?&]{8,}$")

SITE_URL_REGEX = re.compile(r"https://iowa.sharepoint.com/sites/.+")

def regex_validation(string: str, regex: Pattern[str]) -> bool | None:
    """
    Validates regex, used to check sign in creds before connecting to sharepoint
    :param string: String to match
    :param regex: Regex used to match against the string
    :return: True if matches, otherwise none
    """
    return re.fullmatch(regex, string)

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
        cred.web.get_file_by_server_relative_url(download_url).download(sharepoint_file).execute_query()
    if not os.path.exists(download_location):
        os.mkdir(download_location)
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

    with open(full_file_path, "rb") as file:
        file = folder.files.create_upload_session(file, 1000000).execute_query()

    return f"{upload_url}/{os.path.basename(full_file_path)}" == file.serverRelativeUrl
