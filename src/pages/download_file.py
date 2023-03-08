import os

import streamlit as st
import re
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

VALID_EXTENSIONS = (".xls", ".xlsx", ".csv")

PASSWORD_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&]?)[A-Za-z\d@$!%*#?&]{8,}$")

st.session_state['connection-form-disabled'] = False


# TODO
# Determine why changing dropdown runs `on_click`
# Determine why clicking `Log In` button runs `on_click` for `Download` and vice-versa

def download(url: str, file: str, ctx):
    if file != "Select File":
        print(url)

    # cwd = os.getcwd()

    # with open(f"{cwd}/data/temp.xlsx", "wb") as local_file:
    #    ctx.web.get_file_by_server_relative_url(url).download(local_file).execute_query()


def validate(username: str, password: str, site_url: str) -> bool:
    if len(username) < 12 and not username.endswith("@uiowa.edu"):
        return False
    elif not re.fullmatch(PASSWORD_REGEX, password):
        return False
    elif len(site_url) < 48 and not site_url.startswith("https://iowa.sharepoint.com/sites/"):
        return False
    else:
        return True


def create_ctx(username: str, password: str, site_url: str):
    return ClientContext(site_url).with_credentials(UserCredential(username, password))


def add_file_section(username: str, password: str, site_url: str):
    if validate(username, password, site_url):

        st.session_state['connection-form-disabled'] = True

        with st.spinner("Loading Sharepoint Files..."):
            data = get_sharepoint_files(username, password, site_url)

        file = st.selectbox("Select Sharepoint File", options=data)

        st.button(label="Download File", key="download", on_click=download(site_url, file,
                                                                           create_ctx(username, password, site_url)))

    elif len(username) > 0 or len(password) > 0 or len(site_url) > 0:
        st.error("Invalid")


def get_sharepoint_files(username: str, password: str, site_url: str) -> list[str]:
    ctx = create_ctx(username, password, site_url)

    target_folder_url = "Shared Documents"
    root_folder = ctx.web.get_folder_by_server_relative_path(target_folder_url)

    files = root_folder.get_files(True).execute_query()

    data = ["Select File"] + [str(f.properties['ServerRelativeUrl']).split(target_folder_url)[1] for f in files if
                              str(f.properties['ServerRelativeUrl']).endswith(VALID_EXTENSIONS)]

    return data


def set_up_page():
    connection_form = st.form('sharepoint-connection-form')
    username = connection_form.text_input("HawkID", key="username", placeholder="HawkID@uiowa.edu",
                                          disabled=st.session_state['connection-form-disabled'])
    password = connection_form.text_input("HawkID Password", key="password", type="password",
                                          placeholder="HawkID Password",
                                          disabled=st.session_state['connection-form-disabled'])

    site_url = connection_form.text_input("Sharepoint Site URL", key="sharepoint-site",
                                          placeholder="https://iowa.sharepoint.com/sites/<site-name>/",
                                          disabled=st.session_state['connection-form-disabled'])

    connection_form.form_submit_button(label='Login and Connect to Sharepoint',
                                       on_click=add_file_section(username, password, site_url),
                                       disabled=st.session_state['connection-form-disabled'])


set_up_page()
