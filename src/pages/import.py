'''
Render view for import data page

State
-----
view : str
    Current view to be rendered
import_files : list[UploadFile]
    Comes from file uploaded, list of ImportedSheet
alignment_map : list[(str, pd.DataFrame)]
    Alignment columns to select from each dataframe. Created during alignment form step
drop_missing : bool
    Whether or not the user checked drop_missing on alignment column form.
'''
import streamlit as st
import pandas as pd
from utils.html import centered_text
from utils import merge
#from models.imported_sheet import ImportedSheet

IMPORT_PAGE = 0
ALIGNMENT_COLUMNS = 1
MERGE_ALIGNMENT_ROWS = 2
# HELPERS AND FLOW MANAGEMENT

if 'view' not in st.session_state:
    st.session_state['view'] = IMPORT_PAGE

def display_file_upload():
    '''
    Renders the file uploader view
    '''
    def import_data_flow(import_files):
        '''
        Handles render logic when import data submit has occured
        '''
        if len(import_files) == 0 or import_files is None:
            st.write("No files selected!")
        else:
            if not isinstance(import_files, list):
                import_files = [import_files]

            st.session_state['import_files'] = import_files
            st.session_state['view'] = ALIGNMENT_COLUMNS

            st.experimental_rerun()

    st.title("Import Data")
    st.write("Add files to be imported. Multiple files can be selected and the application will attempt to merge them.")
    form = st.form(key="import_data_form")
    files = form.file_uploader('Data Sources:', accept_multiple_files=True, type=[
                               'xlsx', 'csv', 'tsv'])
    form.markdown(centered_text(
        '<em>supports both excel and csv format</em>'), unsafe_allow_html=True)

    submit = form.form_submit_button('Import')

    if submit:
        # Handle imported files.
        import_data_flow(files)


def display_alignment_column_form():
    '''
    Secondary prompt will ask for alignment column to help combine datasets
    '''
    st.header('Select Alignment Columns')
    st.write(
        '''
        Alignment columns are columns with unique data that is consistent between the import files. This may be something such as a student ID column. Please list all variations of this
        column name below within the datasets you selected. These values will be used to determine how rows are merged.
        ''')
    if len(st.session_state.import_files) == 0:
        # No alignment column needed when only one df imported
        st.session_state.view = IMPORT_PAGE
        st.experimental_rerun()

    alignment_form = st.form("alignment_input_form")
    alignment_form.write('**Select 1 column from each file:**')

    alignment_input_map = [] # (col to align, dataframe)

    for file in st.session_state.import_files:
        data = pd.read_excel(file)
        drop_down = alignment_form.selectbox(file.name, data.columns.tolist())
        alignment_input_map.append((drop_down, data))

    drop_missing_checkbox = alignment_form.checkbox('Drop missing?')

    with alignment_form.expander('What does this mean?'):
        st.write(
            '''A row will only be included if the value in its alignment column is present in all your imported data sets.
            For example, if you align the datasets based on the student ID column, a UID present in only 1/2 imported files
            will be dropped if you check "Drop missing"
                 ''')

    alignment_form_submit = alignment_form.form_submit_button("submit")

    if alignment_form_submit:
        # sort in size order
        st.session_state.alignment_map = alignment_input_map
        st.session_state.drop_missing = drop_missing_checkbox

        st.session_state.view = MERGE_ALIGNMENT_ROWS
        st.experimental_rerun()

def display_align_row():
    '''
    Align rows display routine
    '''
    combine_columns = [pair[1][pair[0]] for pair in st.session_state.alignment_map]
    combined_column = merge.combine_columns(combine_columns, st.session_state.drop_missing)

    alignment_columns = [pair[0] for pair in st.session_state.alignment_map]
    alignment_dfs = [pair[1] for pair in st.session_state.alignment_map]
    merge.find_duplicates(alignment_columns, combined_column.tolist()[0], alignment_dfs)


# PAGE RENDER LOGIC
VIEW = st.session_state.view
if VIEW == IMPORT_PAGE:
    display_file_upload()
elif VIEW == ALIGNMENT_COLUMNS:
    display_alignment_column_form()
elif VIEW == MERGE_ALIGNMENT_ROWS:
    display_align_row()
