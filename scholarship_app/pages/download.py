"""
Download file from sharepoint once signed in
"""
import os

import streamlit as st

from scholarship_app.utils.html import redirect
from scholarship_app.sessions.session_manager import SessionManager
from scholarship_app.managers.sharepoint.sharepoint_session import SharepointSession

SESSION = SessionManager(st.session_state, "download", "loading")
SHARE_POINT = SharepointSession(st.session_state)

if not SHARE_POINT.is_signed_in():
    redirect("/Account")

def render_loading_files():
    '''
    Render the loading files spinner
    '''
    with st.spinner("Loading Sharepoint Files..."):
        files = SHARE_POINT.get_files()

    SESSION.set("files", files)
    SESSION.set_view("main")

def render_files_dropdown():
    """
    Sets up the file dropdown, makes sure user is signed in
    """
    if not SESSION.has("files"):
        SESSION.set_view("loading")

    files = SESSION.retrieve("files")
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

st.header("Download A File")

if SESSION.view == "loading":
    render_loading_files()
else:
    render_files_dropdown()
