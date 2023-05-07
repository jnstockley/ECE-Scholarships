"""
Contains shared code for unit tests
"""
from dotenv import dotenv_values
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext


def setup_cred():
    """
    Sets up the creds for logining into SharePoint
    """
    config = dotenv_values(".env")

    # Valid Hawk ID
    hawk_id = config["HAWK_ID"]

    # Valid Password
    hawk_id_password = config["HAWK_ID_PASSWORD"]

    # Valid Sharepoint URL
    sharepoint_url = config["SHAREPOINT_URL"]

    creds: ClientContext = ClientContext(sharepoint_url).with_credentials(
        UserCredential(hawk_id, hawk_id_password)
    )
    creds.web.get().execute_query()

    return creds
