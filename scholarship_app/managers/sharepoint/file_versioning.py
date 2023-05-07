"""
File management with sharepoint utilities

General file structure is as follows
/sharepoint_root/data_type_path/master

Then all user unique files are stored in:
/sharepoint_root/data_type_path/hawk_id/copy
"""
from enum import Enum
import os
import pandas as pd
from scholarship_app.managers.sharepoint.sharepoint_session import SharepointSession
from scholarship_app.sessions.session_manager import SessionManager
from streamlit.runtime.state import SessionStateProxy
from scholarship_app.utils.output import get_appdata_path

SHAREPOINT_ROOT = "scholarship_application"


class DataType(Enum):
    """
    list of potential files we save in sharepoint
    """

    MAIN = "main"
    SCHOLARSHIP = "scholarships"
    REVIEW = "reviews"


class Session(Enum):
    """
    List of session enum keys for storing the users data
    """

    MASTER = "master"
    USER_COPY = "copy"
    USER_COMBINED = "combined"


class DataManager(SessionManager):
    """
    Manages file versioning and storing data in the session.

    Attributes
    ----------
    data_type : DataType
        Data type this data manager is storing
    sharepoint : SharepointSession
        Reference to the active sharepoint session

    """

    def __init__(
        self,
        session: SessionStateProxy,
        data_type: DataType,
        sharepoint: SharepointSession,
    ):
        super().__init__(session, f"data_{data_type.name}", "default")

        self.data_type = data_type
        self.sharepoint = sharepoint
        self.relative_path = os.path.join(SHAREPOINT_ROOT, data_type.value)
        # makes the directory
        get_appdata_path(self.relative_path)

        self.master_path = os.path.join(self.relative_path, "master.xlsx")
        self.user_path = os.path.join(self.relative_path, self.sharepoint.get_hawk_id())
        # makes the directory
        get_appdata_path(self.user_path)

        self.user_copy_path = os.path.join(
            self.user_path, f"{self.sharepoint.get_hawk_id()}/copy.xlsx"
        )

    def retrieve_master(self) -> pd.DataFrame | None:
        """
        Retrieves the master dataset if available
        """
        if self.has(Session.MASTER):
            return self.retrieve(Session.MASTER)

        if self.__in_appdata(self.master_path):
            data = self.retrieve_appdata_file(self.master_path)
            self.set(Session.MASTER, data)

            return data

        if self.__in_sharepoint(self.master_path):
            self.sharepoint.download(self.master_path, self.master_path)

            data = self.retrieve_appdata_file(self.master_path)
            self.set(Session.MASTER, data)

            return data

        return None

    def set_master(self, data: pd.DataFrame):
        """
        Updates the master data in appdata, sharepoint and session. Will overwrite previous version
        if it exists.
        """
        app_data_dir = os.path.join(get_appdata_path(), self.master_path)
        data.to_excel(app_data_dir, index=False)

        self.sharepoint.upload(self.master_path, self.relative_path)
        self.set(Session.MASTER, data)

    def retrieve_appdata_file(self, path: str) -> pd.DataFrame:
        """
        Retrieve the dataframe from appdata. Path is relative to appdata root
        """
        if not self.__in_appdata(self.master_path):
            raise FileExistsError(f"Path: {path} does not exist in appdata!")

        path = os.path.join(get_appdata_path(), path)
        return pd.read_excel(path)

    def __in_appdata(self, path: str) -> bool:
        """
        Checks if path is in appdata?
        """
        appdata_relative_path = os.path.join(get_appdata_path(), path)
        return os.path.exists(appdata_relative_path)

    def __in_sharepoint(self, path: str) -> bool:
        """
        Checks if path is in sharepoint
        """
        return self.sharepoint.has_file(path)
