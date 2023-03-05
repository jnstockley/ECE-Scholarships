'''
Render view for import data page
'''
import streamlit as st
import pandas as pd
from utils.html import centered_text
from utils import merge

IMPORT_PAGE = 0
ALIGNMENT_COLUMNS = 1
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
            print(st.session_state['view'])

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
    alignment_columns_input = alignment_form.text_input(label='columns')
    alignment_form.write('**separate columns with ","**')
    alignment_form.write('*for example: "UID,UID.1,student_id" would be a valid input.*')
    alignment_form_submit = alignment_form.form_submit_button("submit")

    if alignment_form_submit:
        alignment_columns = [word.strip().lower()
                             for word in alignment_columns_input.split(',')]
        datasets = [pd.read_excel(file)
                    for file in st.session_state.import_files]

        # Verify each column exists once in each dataset.
        valid_input = True
        for data in datasets:
            columns = [col.lower() for col in data.columns]
            found = False

            for alignment_column in alignment_columns:
                if alignment_column in columns:
                    found = True
                    break

            if not found:
                valid_input = False
                break

        if not valid_input:
            st.write(
                "An inputted column was not found in any dataset. Please retry")
            return

        # do alignment thingys
        #update_merge_columns()
        merge.align_dfs_along_columns(alignment_columns, datasets)
        st.experimental_rerun()

# PAGE RENDER LOGIC
VIEW = st.session_state.view
if VIEW == IMPORT_PAGE:
    display_file_upload()
elif VIEW == ALIGNMENT_COLUMNS:
    display_alignment_column_form()
