'''
Contains objects which make managing the import data session information
easier.
'''
from enum import Enum
import streamlit as st
from streamlit.runtime.state import SessionStateProxy
from src.sessions.session_manager import SessionManager
from src.models.imported_sheet import ImportedSheet
from src.managers.import_data.alignment_settings import AlignmentInfo
from src.managers.import_data.similar_columns import MergeSimilarManager

class Session(Enum):
    '''
    Session keys stored as enums
    '''
    # Main dataframe merged along the alignment_columns
    VIEW = "view"
    ALIGNED_DF = "aligned_dataframe"
    IMPORTED_SHEETS = "imported_sheets"
    ALIGNMENT_INFO = "alignment_info"
    SIMILAR_MANAGER = "similar_manager"
    FINAL_DATA = "final_data"

class View(Enum):
    '''
    Different view states represented as enums
    '''
    IMPORT_PAGE = 0
    ALIGNMENT_COLUMNS = 1
    DUPLICATE_COLUMN_HANDLER = 2
    MERGE_COLUMNS = 3
    IMPORT_COMPLETE = 4

class ImportSessionManager(SessionManager):
    '''
    Main import view session manager. Offloads any backend logic from the UI codebase.

    Attributes
    ----------
    view : View
        One of the possible enum views. Indiciates what view to render in the UI
    imported_sheets : list[ImportedSheet] | none
        The imported sheet objects linked to files the user imported.
    aligned_df : pd.Dataframe
        The combined dataframe along a single alignment column
    alignment_info : AlignmentInfo
        The alignment information relevant when the user is selecting how data is aligned for the alignment column.
    similar : MergeSimilarManager
        Reference to the similar column merge manager.
    '''
    def __init__(self, session: SessionStateProxy):
        super().__init__(session)

        if not self._has(Session.VIEW):
            self._set(Session.VIEW, View.IMPORT_PAGE)

        self.view = self._retrieve(Session.VIEW)

        if self._has(Session.IMPORTED_SHEETS):
            self.imported_sheets = self._retrieve(Session.IMPORTED_SHEETS)

        if self._has(Session.ALIGNED_DF):
            self.aligned_df = self._retrieve(Session.ALIGNED_DF)

        if self._has(Session.ALIGNMENT_INFO):
            self.alignment_info = self._retrieve(Session.ALIGNMENT_INFO)

        if self._has(Session.SIMILAR_MANAGER):
            self.similar = self._retrieve(Session.SIMILAR_MANAGER)

    def import_sheets(self, files: list[ImportedSheet]):
        '''
        Import sheets to use for further steps.
        '''
        if len(files) == 0:
            raise IOError("No files imported!")

        self._set(Session.IMPORTED_SHEETS, [ImportedSheet(file) for file in files])
        self.imported_sheets = self._retrieve(Session.IMPORTED_SHEETS)

    def set_view(self, view: View):
        '''
        Sets current page view
        '''
        self._set(Session.VIEW, view)
        st.experimental_rerun()

    def has_aligned_df(self) -> bool:
        '''
        Checks whether the alignment column df has been added
        '''
        return self._has(Session.ALIGNED_DF)

    def complete_aligned_df(self):
        '''
        Sets aligned dataframe to session. Moves to merge columns view.
        '''
        if self.alignment_info is None:
            raise NameError('alignment_info missing from session')

        aligned_df = self.alignment_info.get_aligned_df()
        self._set(Session.ALIGNED_DF, aligned_df)
        self._set(Session.SIMILAR_MANAGER, MergeSimilarManager(self.alignment_info.info.final_column_name, aligned_df))
        self.set_view(View.MERGE_COLUMNS)

    def begin_alignment(self, alignment_info: AlignmentInfo):
        '''
        Begin the alignment column flow
        '''
        self._set(Session.ALIGNMENT_INFO, alignment_info)
        self.set_view(View.DUPLICATE_COLUMN_HANDLER)

    def complete_import(self):
        '''
        Completes the import flow and sets final data.
        '''
        self._set(Session.FINAL_DATA, self.aligned_df)
