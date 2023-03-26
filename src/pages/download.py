import os
import time

from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext

from utils.cookies import get_manager
import streamlit as st

VALID_EXTENSIONS = (".xls", ".xlsx", ".csv")


def redirect(url: str):
    st.write(f'<meta http-equiv="refresh" content="0; url={url}">', unsafe_allow_html=True)


def connect_to_sharepoint(hawkid: str, password: str, site_url: str):
    creds = ClientContext(site_url).with_credentials(UserCredential(hawkid, password))
    try:
        web = creds.web.get().execute_query()
    except IndexError:
        return None
    except ClientRequestException:
        return None
    if f"{web.url}/" == site_url:
        return creds
    else:
        return None


def get_sharepoint_files(ctx):
    target_folder_url = "Shared Documents"
    root_folder = ctx.web.get_folder_by_server_relative_path(target_folder_url)

    files = root_folder.get_files(True).execute_query()

    data = ["Select File"] + [str(f.properties['ServerRelativeUrl']).split(target_folder_url)[1] for f in files if
                              str(f.properties['ServerRelativeUrl']).endswith(VALID_EXTENSIONS)]

    return data


def download_file(site_url: str, file_path: str, ctx):
    full_url = f"{site_url.replace('https://iowa.sharepoint.com', '')}Shared Documents{file_path}"

    cwd = os.getcwd()

    with open(f"{cwd}/data/temp.xlsx", "wb") as local_file:
        ctx.web.get_file_by_server_relative_url(full_url).download(local_file).execute_query()


def files_dropdown():
    if cookie_manager.get('cred') is None:
        redirect("/Log%20In")

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
