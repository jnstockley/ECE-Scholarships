"""
Download file from sharepoint once signed in
"""
import os
import time

import streamlit as st

from src.utils.html import redirect
from enum import Enum
from src.sessions.session_manager import SessionManager, GlobalSession
from src.managers.sharepoint.sharepoint_session import SharepointSession

class DownloadView(Enum):
    '''
    Download page views
    '''
    LOADING_FILES = "loading"
    MAIN = "main"

class SessionKey(Enum):
    '''
    Global shared sessions
    '''
    FILES = "files"

SESSION = SessionManager(st.session_state, "LOADING_FILES")
SHARE_POINT = SharepointSession(st.session_state)

if not SHARE_POINT.is_signed_in():
    redirect("/Account")

def render_loading_files():
    '''
    Render the loading files spinner
    '''
    with st.spinner("Loading Sharepoint Files..."):
        files = SHARE_POINT.get_files()

    SESSION.set(SessionKey.FILES, files)
    SESSION.set_view("MAIN")

def render_files_dropdown():
    """
    Sets up the file dropdown, makes sure user is signed in
    """
    if not SESSION.has(SessionKey.FILES):
        SESSION.set_view("LOADING_FILES")
        st.experimental_rerun()

    files = SESSION.retrieve(SessionKey.FILES)
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

if SESSION.view == "LOADING_FILES":
    render_loading_files()
else:
    render_files_dropdown()
