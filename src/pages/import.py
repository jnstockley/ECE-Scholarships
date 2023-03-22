'''
Render view for import data page

State
-----
alignment_map : list[(str, pd.DataFrame)]
    Alignment columns to select from each dataframe. Created during alignment form step
drop_missing : bool
    Whether or not the user checked drop_missing on alignment column form.
final_column_name_input : str
    Name of the alignment column in the combined dataset
check_duplicate_column_index : int
    Row index to check for duplicate columns
final_alignment_column : pd.Series
    The final alignment column in the output merged DF
duplicate_column_comparison_details : (str, dict[str, pd.DataFrame])
    Contains a tuple with first element being value of the alignment column row data it found duplicate with
    mismatched data for, and second element are the tables, where str is duplicate column name, and the value is
    an associated dataframe with the varying values displayed.
radio_duplicate_column_selections : (str, any)
    (Column name, selected value to keep for that duplicate column)
aligned_dataframe : pd.Dataframe
    The combined dataframe along a single alignment column.
'''
import streamlit as st
from src.utils.html import centered_text
from src.utils import merge
from src.sessions.import_session_manager import ImportSessionManager, View
from src.managers.alignment_settings import SelectAlignment, AlignmentManager

# HELPERS AND FLOW MANAGEMENT
SESSION = ImportSessionManager(st.session_state)

def display_file_upload():
    '''
    Renders the file uploader view
    '''
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
        if not files:
            SESSION.set_view(View.IMPORT_PAGE)

        SESSION.import_sheets(files)
        SESSION.set_view(View.ALIGNMENT_COLUMNS)


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
    if len(SESSION.imported_sheets) <= 1:
        if len(SESSION.imported_sheets) == 1:
            # one sheet, set as the combined "alignment" sheet
            st.session_state.aligned_dataframe = SESSION.imported_sheets[0].get_df()
            update_merge_columns()
            SESSION.set_view(View.MERGE_COLUMNS)
        else:
            # No alignment column needed when only one df imported
            SESSION.set_view(View.IMPORT_COMPLETE)

    alignment_form = st.form("alignment_input_form")
    alignment_form.write('**Select 1 column from each file:**')

    alignment_inputs = [] # (col to align, dataframe)

    for sheet in SESSION.imported_sheets:
        data = sheet.get_df()
        drop_down = alignment_form.selectbox(sheet.file_name, data.columns.tolist())
        alignment_inputs.append(SelectAlignment(drop_down, sheet))

    drop_missing_checkbox = alignment_form.checkbox('Drop missing?')

    with alignment_form.expander('What does this mean?'):
        st.write(
            '''A row will only be included if the value in its alignment column is present in all your imported data sets.
            For example, if you align the datasets based on the student ID column, a UID present in only 1/2 imported files
            will be dropped if you check "Drop missing"
                 ''')

    final_column_name_input = alignment_form.text_input('Final column name:')
    alignment_form_submit = alignment_form.form_submit_button("submit")

    if alignment_form_submit:
        if final_column_name_input.strip() == '':
            st.write('Error: please specify your final combined alignment column name')
            return

        alignment_info = AlignmentManager(drop_missing_checkbox, final_column_name_input, alignment_inputs)
        SESSION.begin_alignment(alignment_info)

def display_duplicate_column_form():
    '''
    Align rows display routine
    '''
    alignment_info: AlignmentManager = SESSION.alignment_info
    #print(f"Remaining mismatches = {len(alignment_info._mismatched_duplicate_column_row)}")

    if alignment_info.alignment_complete():
        return

    if not alignment_info.session_has_duplicate():
        alignment_info.pop_next_duplicate_to_handle()

    duplicate_details = alignment_info.current_duplicate_details

    st.header('Duplicate Column(s) Found')
    duplicate_handler_form = st.form(key='duplicate_column_form')
    duplicate_handler_form.write(f'For the unique alignment column value {duplicate_details.alignment_row_value}, please select which data to keep:')
    duplicate_handler_form.write('### Columns')

    duplicate_handler_form.write(f'_{duplicate_details.duplicate_column_name}:_')
    col1, col2 = duplicate_handler_form.columns(2)
    with col1:
        st.dataframe(duplicate_details.get_comparison_df())
    with col2:
        st.radio(f"Select the final value for column '{duplicate_details.duplicate_column_name}'",
            duplicate_details.get_values())

    # Once the value is selected, go through each df and find the column if it has it and set the value to the selected value
    next_button = duplicate_handler_form.form_submit_button('Next')
    if next_button:
        # st.session_state.duplicate_column_comparison_details = None
        # for duplicate_col_input in mapped_data_inputs:
        #     merge.replace_alignment_row_duplicate_column_value(duplicate_details[0], duplicate_col_input[1], duplicate_col_input[0], alignment_columns, alignment_sheets)
        st.experimental_rerun()
    else:
        return

    # find_next_duplicate_column(alignment_columns, alignment_sheets, max_col_index)

def update_merge_columns():
    '''
    Refreshes merge columns based on state
    '''
    import_dfs = [st.session_state.aligned_dataframe]
    columns = [column for data in import_dfs for column in data.columns]

    merge_columns = merge.find_similar_columns(columns, 70)
    st.session_state['merge_fields'] = merge_columns


def display_merge_form(merge_details):
    '''
    Renders a single merge popup
    '''
    st.header("Duplicate Columns Have Been Detected")
    st.write("Please select how you'd like these duplicates to be handled")
    st.write(f"_{len(st.session_state['merge_fields'])} remaining..._")

    merge_form = st.form(key="merge_data_form")
    merge_columns = [merge_details[0]] + merge_details[1]

    col1, col2, col3 = merge_form.columns(3)
    with col1:
        st.header("Merge:")
        st.write(merge_columns)
    with col2:
        st.write("arrow ->")
    with col3:
        st.header("To:")
        st.write(merge_details[0])

    merge_button = merge_form.form_submit_button('merge')
    skip_button = merge_form.form_submit_button('skip')

    merge_form.dataframe(st.session_state.aligned_dataframe[merge_columns])

    if skip_button:
        # skip should have priority
        pass
    elif merge_button:
        # Merge will need to handle updating the state if that column
        # is similar to another. It should merge DB and then re-run duplicates.
        pass

def display_done_view():
    '''
    Import completed view
    '''
    st.write('import completed!')
    import_another = st.button('import another')

    if import_another:
        SESSION.set_view(View.IMPORT_PAGE)

# PAGE RENDER LOGIC
if SESSION.view == View.IMPORT_PAGE:
    display_file_upload()
elif SESSION.view == View.ALIGNMENT_COLUMNS:
    display_alignment_column_form()
elif SESSION.view == View.DUPLICATE_COLUMN_HANDLER:
    display_duplicate_column_form()
elif SESSION.view == View.MERGE_COLUMNS:
    if len(st.session_state.merge_fields) > 0:
        display_merge_form(st.session_state.merge_fields.pop(0))
    else:
        pass  # skip to next view
elif SESSION.view == View.IMPORT_COMPLETE:
    display_done_view()
