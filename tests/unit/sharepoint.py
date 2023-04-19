"""
Tests for SharePoint functions
"""
import os
import unittest

from dotenv import dotenv_values
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

from src.utils.sharepoint import get_files, download, upload



class SharepointTest(unittest.TestCase):
    """
    Unit test for SharePoint
    """

    def setUp(self) -> None:
        """
        Logs the user in to use to ensure sharepoint functions work
        """

        config = dotenv_values(".env")

        # Valid Hawk ID
        hawk_id = config["HAWK_ID"]

        # Valid Password
        hawk_id_password = config["HAWK_ID_PASSWORD"]

        # Valid Sharepoint URL
        sharepoint_url = "https://iowa.sharepoint.com/sites/SEP2023-Team2/" # config["SHAREPOINT_URL"]

        self.creds: ClientContext = ClientContext(sharepoint_url).with_credentials(UserCredential(hawk_id,
                                                                                                  hawk_id_password))

        self.web = self.creds.web.get().execute_query()

    def test_get_files(self):
        """
        Test for `get_files`
        """
        files = get_files(self.creds)

        assert len(files) >= 4
        assert "/Team 2/test.xlsx" in files

    def test_download(self):
        """
        Test for `download`
        """
        downloaded = download('/Team 2/test.xlsx', f'{os.getcwd()}/.app_data/', self.creds)

        assert downloaded

    def test_upload(self):
        """
        Test for `upload`
        """
        uploaded = upload(f'{os.getcwd()}/tests/data/test.xlsx', '/Team 2/Test Directory', self.creds)

        assert uploaded


if __name__ == "__main__":
    unittest.main()
