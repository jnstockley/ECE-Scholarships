
from office365.runtime.auth.token_response import TokenResponse
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

from pages import app_config
import tempfile
import os

import streamlit as st


def redirect(url):
    st.write(f'<meta http-equiv="refresh" content="0; url={url}">', unsafe_allow_html=True)


if st.button("Login"):
    authority_url = app_config.AUTHORITY
    import msal

    app = msal.ConfidentialClientApplication(
        authority=authority_url,
        client_id=app_config.CLIENT_ID,
        client_credential=app_config.CLIENT_SECRET
    )
    token_json = app.acquire_token_for_client(scopes=["https://mediadev8.sharepoint.com/.default"])
    temp = TokenResponse.from_json(token_json)
    site = "https://iowa.sharepoint.com/sites/SEP2023-Team2/"
    ctx = ClientContext(site).with_credentials(UserCredential(app_config.USERNAME, app_config.PASSWORD))


    def enum_folder(parent_folder, fn):
        """
        :type parent_folder: Folder
        :type fn: (File)-> None
        """
        parent_folder.expand(["Files", "Folders"]).get().execute_query()
        for file in parent_folder.files:  # type: File
            fn(file)
        for folder in parent_folder.folders:  # type: Folder
            enum_folder(folder, fn)


    def print_file(f):
        """
        :type f: File
        """
        print(f.properties['ServerRelativeUrl'])


    target_folder_url = "Shared Documents/Team 2"
    root_folder = ctx.web.get_folder_by_server_relative_path(target_folder_url)
    # enum_folder(root_folder, print_file)

    files = root_folder.get_files(True).execute_query()
    [print_file(f) for f in files]

    file_url = "/sites/SEP2023-Team2/Shared Documents/Team 2/Test Plan.pptx"
    download_path = os.path.join(tempfile.mkdtemp(), os.path.basename(file_url))
    with open(download_path, "wb") as local_file:
        file = ctx.web.get_file_by_server_relative_url(file_url).download(local_file).execute_query()
        # file = ctx.web.get_file_by_server_relative_url(file_url).download(local_file).execute_query()
    print("[Ok] file has been downloaded into: {0}".format(download_path))
