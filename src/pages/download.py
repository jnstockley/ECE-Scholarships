"""
Download file from sharepoint once signed in
"""
import os
import time

import streamlit as st

from src.pages.login import redirect
from src.utils.sharepoint import login, get_files, download, logged_in

# List of valid files to download from sharepoint
VALID_EXTENSIONS = (".xls", ".xlsx", ".csv")


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

    if not logged_in():
        redirect("/Log%20In")
        return

    with st.spinner("Loading Sharepoint Files..."):

        creds = login()

        files = get_files(creds)

    file_selector = st.form('sharepoint-file-selector')

    file = file_selector.selectbox("Select File", options=files)

    if file_selector.form_submit_button("Download File"):
        if file != "Select File":
            download(file)
        else:
            file_selector.error("Invalid File Selected")


time.sleep(.2)


files_dropdown()
