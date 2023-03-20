'''
Render view for import data page

State
-----
view : str
    Current view to be rendered
imported_sheets : list[ImportedSheet]
    Comes from file uploaded, list of ImportedSheet
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
'''
import streamlit as st
from src.utils.html import centered_text
from src.utils import merge
from src.models.imported_sheet import ImportedSheet

IMPORT_PAGE = 0
ALIGNMENT_COLUMNS = 1
DUPLICATE_COLUMN_HANDLER = 2
IMPORT_COMPLETE = 4
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

            st.session_state.imported_sheets = [ImportedSheet(file) for file in import_files]
            st.session_state.view = ALIGNMENT_COLUMNS

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

def display_scholarship_import():
    st.title("Import Scholarships")
    st.write("Add files to be imported. This should be of the form ECE_SCHOLARSHIPS_SPRING_2023")

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
    if len(st.session_state.imported_sheets) == 0:
        # No alignment column needed when only one df imported
        st.session_state.view = IMPORT_PAGE
        st.experimental_rerun()

    alignment_form = st.form("alignment_input_form")
    alignment_form.write('**Select 1 column from each file:**')

    alignment_input_map = [] # (col to align, dataframe)

    for sheet in st.session_state.imported_sheets:
        data = sheet.get_df()
        drop_down = alignment_form.selectbox(sheet.file_name, data.columns.tolist())
        alignment_input_map.append((drop_down, sheet))

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
        # sort in size order
        st.session_state.alignment_map = alignment_input_map
        st.session_state.drop_missing = drop_missing_checkbox
        st.session_state.alignment_column_name = final_column_name_input

        combine_columns = [pair[1].get_df()[pair[0]] for pair in alignment_input_map]
        st.session_state.final_alignment_column = merge.combine_columns(combine_columns, drop_missing_checkbox)

        st.session_state.view = DUPLICATE_COLUMN_HANDLER
        st.experimental_rerun()

def find_next_duplicate_column(alignment_columns: list[str], alignment_sheets: list[ImportedSheet], max_col_index: int):
    '''
    Checks each alignment value row to find any columns with duplicate data that is different between datasets. Will flag this
    to be rendered in the duplicate column UI by assigned a value to st.session_state.duplicate_column_comparison_details.
    Will stop once max_col_index reached.
    '''
    column_data_comparison_tables = {}
    alignment_col_row_value = None

    while len(column_data_comparison_tables.items()) == 0 and st.session_state.check_duplicate_column_index <= max_col_index:
        alignment_col_row_value = st.session_state.final_alignment_column.tolist()[st.session_state.check_duplicate_column_index]
        column_data_comparison_tables = merge.find_duplicates(alignment_columns, alignment_col_row_value, alignment_sheets)
        st.session_state.check_duplicate_column_index +=1

    if len(column_data_comparison_tables.items()) > 0:
        st.session_state.duplicate_column_comparison_details = (alignment_col_row_value, column_data_comparison_tables)

    st.experimental_rerun()

def display_duplicate_column_form():
    '''
    Align rows display routine
    '''
    if 'check_duplicate_column_index' not in st.session_state:
        st.session_state.check_duplicate_column_index = 0

    alignment_columns = [pair[0] for pair in st.session_state.alignment_map]
    alignment_sheets = [pair[1] for pair in st.session_state.alignment_map]
    max_col_index = len(st.session_state.final_alignment_column.tolist())-1

    if max_col_index < st.session_state.check_duplicate_column_index:
        st.session_state.view = IMPORT_COMPLETE
        merged_data = merge.merge_with_alignment_columns(st.session_state.alignment_column_name, alignment_columns, st.session_state.final_alignment_column, alignment_sheets)
        print(merged_data)
        st.experimental_rerun()

    if 'duplicate_column_comparison_details' in st.session_state and st.session_state.duplicate_column_comparison_details is not None:
        duplicate_details = st.session_state.duplicate_column_comparison_details
        st.header('Duplicate Column(s) Found')
        duplicate_handler_form = st.form(key='duplicate_column_form')
        duplicate_handler_form.write(f'For the alignment column value {duplicate_details[0]}, please select which data to keep:')
        duplicate_handler_form.write('### Columns')

        # (duplicate column name, value)
        mapped_data_inputs = []

        for i, column_name in enumerate(duplicate_details[1]):
            duplicate_handler_form.write(f'_{column_name}:_')
            col1, col2 = duplicate_handler_form.columns(2)
            with col1:
                st.dataframe(duplicate_details[1][column_name])
            with col2:
                radio_select = st.radio(f"Select the final value for column '{column_name}'",
                    duplicate_details[1][column_name].loc['Values', :].tolist())

                mapped_data_inputs.append((column_name, radio_select))


            if i < len(duplicate_details[1])-1:
                duplicate_handler_form.write('---')

        # Once the value is selected, go through each df and find the column if it has it and set the value to the selected value
        next_button = duplicate_handler_form.form_submit_button('Next')
        if next_button:
            st.session_state.duplicate_column_comparison_details = None
            for duplicate_col_input in mapped_data_inputs:
                merge.replace_alignment_row_duplicate_column_value(duplicate_details[0], duplicate_col_input[1], duplicate_col_input[0], alignment_columns, alignment_sheets)
            st.experimental_rerun()
        else:
            return

    find_next_duplicate_column(alignment_columns, alignment_sheets, max_col_index)

def display_done_view():
    '''
    Import completed view
    '''
    st.write('import completed!')
    import_another = st.button('import another')

    if import_another:
        st.session_state.view = IMPORT_PAGE
        st.experimental_rerun()

# PAGE RENDER LOGIC
VIEW = st.session_state.view
if VIEW == IMPORT_PAGE:
    display_file_upload()
    display_scholarship_import()
elif VIEW == ALIGNMENT_COLUMNS:
    display_alignment_column_form()
elif VIEW == DUPLICATE_COLUMN_HANDLER:
    display_duplicate_column_form()
elif VIEW == IMPORT_COMPLETE:
    display_done_view()
