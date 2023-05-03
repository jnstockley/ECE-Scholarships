"""
Download file from sharepoint once signed in
"""
import os
import time

import streamlit as st

from src.utils.html import redirect
from src.managers.sharepoint.sharepoint_session import SharepointSession

SHARE_POINT = SharepointSession(st.session_state)
if not SHARE_POINT.is_signed_in():
    redirect("/Account")

def files_dropdown():
    """
    Sets up the file dropdown, makes sure user is signed in
    """

    st.header("Download A File")

    with st.spinner("Loading Sharepoint Files..."):
        files = SHARE_POINT.get_files()

    file_selector = st.form('sharepoint-file-selector')

    file = file_selector.selectbox("Sharepoint Files", options=files)

    if file_selector.form_submit_button("Download File"):
        if file != "Select File":
            downloaded = SHARE_POINT.download(file, f"{os.getcwd()}/data/")
            if downloaded:
                file_selector.info(f"Downloaded {file}")
                return
            file_selector.error(f"Error downloading {file}")
            return
        file_selector.error("Invalid File Selected")
        return


time.sleep(.2)


files_dropdown()
