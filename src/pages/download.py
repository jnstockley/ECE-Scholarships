"""
Download file from sharepoint once signed in
"""
import os
import time

from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext

import streamlit as st

from src.pages.login import redirect
from src.utils.cookies import get_manager


# List of valid files to download from sharepoint
VALID_EXTENSIONS = (".xls", ".xlsx", ".csv")


def connect_to_sharepoint(hawkid: str, password: str, site_url: str):
    """
    Connects and signs into the SharePoint site
    :param hawkid: Username
    :param password: Password
    :param site_url: Sharepoint Site URL
    :return: CTX which managers the login and connection to sharepoint
    """
    creds = ClientContext(site_url).with_credentials(UserCredential(hawkid, password))
    try:
        web = creds.web.get().execute_query()
    except IndexError:
        return None
    except ClientRequestException:
        return None
    if f"{web.url}/" == site_url:
        return creds
    return None


def get_sharepoint_files(ctx):
    """
    Gets a list of files from the sharepoint site
    :param ctx: Session manager to manager connection with SharePoint
    :return: List of valid files that can be downloaded
    """
    target_folder_url = "Shared Documents"
    root_folder = ctx.web.get_folder_by_server_relative_path(target_folder_url)

    files = root_folder.get_files(True).execute_query()

    data = ["Select File"] + [str(f.properties['ServerRelativeUrl']).split(target_folder_url)[1] for f in files if
                              str(f.properties['ServerRelativeUrl']).endswith(VALID_EXTENSIONS)]

    return data


def download_file(site_url: str, file_path: str, ctx):
    """
    Downlaods the specific file from the sharepoint site
    :param site_url: Full URL to Sharepoint site
    :param file_path: Path to File in SharePoint
    :param ctx: Session manager to manager connection with SharePoint
    """
    full_url = f"{site_url.replace('https://iowa.sharepoint.com', '')}Shared Documents{file_path}"

    cwd = os.getcwd()

    with open(f"{cwd}/data/temp.xlsx", "wb") as local_file:
        ctx.web.get_file_by_server_relative_url(full_url).download(local_file).execute_query()


def files_dropdown():
    """
    Sets up the file dropdown, makes sure user is signed in
    """

    st.header("Download A File")

    if cookie_manager.get('cred') is None:
        redirect("/Log%20In")
        return

    cookie_creds = cookie_manager.get('cred')

    with st.spinner("Loading Sharepoint Files..."):

        creds = connect_to_sharepoint(cookie_creds['hawk-id'], cookie_creds['password'], cookie_creds['site-url'])

        files = get_sharepoint_files(creds)

    file_selector = st.form('sharepoint-file-selector')

    file = file_selector.selectbox("Select File", options=files)

    if file_selector.form_submit_button("Download File"):
        if file != "Select File":
            download_file(cookie_creds['site-url'], file, creds)
        else:
            file_selector.error("Invalid File Selected")


cookie_manager = get_manager()


time.sleep(.2)


files_dropdown()
