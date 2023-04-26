"""
Download file from sharepoint once signed in
"""
import os
import time

import streamlit as st

from scholarship_app.utils.html import redirect
from scholarship_app.utils.sharepoint import login, get_files, download, logged_in


def files_dropdown():
    """
    Sets up the file dropdown, makes sure user is signed in
    """

    st.header("Download A File")

    cookie = logged_in()

    if not cookie:
        redirect("/Log%20In")
        return

    with st.spinner("Loading Sharepoint Files..."):

        creds = login(cookie)

        files = get_files(creds)

    file_selector = st.form('sharepoint-file-selector')

    file = file_selector.selectbox("Select File", options=files)

    if file_selector.form_submit_button("Download File"):
        if file != "Select File":
            downloaded = download(file, f"{os.getcwd()}/data/", creds)
            if downloaded:
                file_selector.info(f"Downloaded {file}")
                return
            file_selector.error(f"Error downloading {file}")
            return
        file_selector.error("Invalid File Selected")
        return


time.sleep(.2)


files_dropdown()
