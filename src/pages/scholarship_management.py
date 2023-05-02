"""
scholarship management page render
"""
import os
import streamlit as st
from streamlit_extras.stateful_button import button
import pandas as pd
from src.utils.html import centered_text, redirect
from src.utils.scholarship_management import read_rows, write_rows, edit_row, groups_string_to_list, check_columns_equal, equalize_dictionary_columns
from src.utils.sharepoint import logged_in, login

cookie = logged_in()

if not cookie:
    redirect("/Log%20In")

@st.cache_data
def download_data():
    # Initializing data
    creds = login(cookie)
    master_sheet = read_rows('data/Master_Sheet.xlsx', creds)
    st.session_state.master_sheet = master_sheet
    try:
        scholarships = read_rows('data/Scholarships.xlsx', creds)
        st.session_state.scholarships = scholarships
    except FileNotFoundError:
        write_rows(pd.DataFrame({}), 'data/Scholarships.xlsx', 'Scholarships', creds)
        st.session_state.scholarships = pd.DataFrame({})
    return creds, scholarships, master_sheet
creds, scholarships, master_sheet = download_data()

if 'scholarships' not in st.session_state:
    st.session_state.scholarships = scholarships
scholarships = st.session_state.scholarships

# st.session_state.scholarships = scholarships
# scholarships = st.session_state.scholarships

# This is for determining how many groups have been added to a scholarship
# Needed because of experimental_rerun() call to allow as many groups as they want
if 'n_groups' not in st.session_state:
    st.session_state.n_groups = 0


# Global variables; SCH_COLUMNS contains all the columns that can be in a scholarship, majors contains all the majors,
# group options is all the column names that can be selected for a group
# and group help is the help message when hovering over the ? on a group field.
SCH_COLUMNS = master_sheet.columns.tolist()
MAJORS = ['Computer Science and Engineering', 'Electrical Engineering', 'All']
GROUP_OPTIONS = ['RAI', 'Admit Score', 'Major', 'ACT Math', 'ACT English', 'ACT Composite',
                 'SAT Math', 'SAT Reading', 'SAT Combined', 'GPA', 'HS Percentile']
GROUP_HELP = """A requirement grouping groups the selected requirements so only one is required.
            i.e. ACT Composite, SAT Combined, HS Percentile all being selected requires only the 
            minimum requirement of ACT Composite, SAT Combined, or HS Percentile."""


def display_create_dynamic():
    '''
    This function displays all of the associated view/actions for creating a scholarship
    with dynamic columns and adding it to the scholarship file.
    '''
    st.title('Create a New Scholarship')
    col_values = {}
    # These 3 fields are always a necessity
    name = st.text_input("Scholarship Name", max_chars=500, placeholder="Enter Scholarship Name")
    total = st.text_input("Total amount of Scholarships", max_chars=8, placeholder="Enter Numerical Amount")
    value = st.text_input('The value of each individual Scholarship', max_chars=8, placeholder="Enter Numerical Amount")
    col_values['Name'] = name
    col_values['Total Amount'] = total
    col_values['Value'] = value
    # Every time a value is selected in the criteria multiselect it gets a display
    dyn_columns = st.multiselect("Choose Relevant Criteria to this Scholarship", options=SCH_COLUMNS, help='''Every criteria you select
                                 will create a new enter field for you to put the relevant value in.''')
    for val in dyn_columns:
        chosen_val = st.text_input('Enter the minimum ' + val + ' requirement')
        col_values[val] = chosen_val
    # Every time the button is pressed we increment the group count and rerun the script
    if st.button('Add a Requirement Grouping', key='Add a Requirement Grouping'):
        st.session_state.n_groups += 1
        st.experimental_rerun()
    # Load as many groups equal to their button presses
    for i in range(st.session_state.n_groups):
        group = st.multiselect("Choose Group " + str(i+1), options=GROUP_OPTIONS, help=GROUP_HELP)
        col_values["Group" + str(i+1)] = group

    if st.button('Create Scholarship', key='Create Scholarship'):
        # These fields should not be able to be blank
        if name == "" or total == "" or value == "":
            st.write("Please make sure all the fields are filled out.")
        else:
            #col_values needs to have any missing columns set to None so it can be added
            equalize_dictionary_columns(SCH_COLUMNS, col_values)
            # pd.Series creates a Panda object that can be appended to the scholarships dataframe.
            scholarship = pd.Series(col_values, name = scholarships.shape[0])
            # We need to go through all the previous scholarships and make sure if a column was added after
            # they were added, we add that column to the scholarship and initialize it as None
            new_scholarships = pd.DataFrame({})
            for i in range(scholarships.shape[0]):
                dict_sch = scholarships.loc[i].to_dict()
                equalize_dictionary_columns(SCH_COLUMNS, dict_sch)
                updated_sch = pd.Series(dict_sch, name = i)
                # Append the new version of the scholarship (might be the same if no new columns) to our new dataframe
                new_scholarships = new_scholarships.append(updated_sch)
            # Append the newly created scholarship to the new dataframe and write it to the file
            new_scholarships = new_scholarships.append(scholarship)
            write_rows(new_scholarships, 'data/Scholarships.xlsx', 'Scholarships', creds)
            st.session_state.scholarships = new_scholarships
            st.write(name + " has been successfully created.")

def display_edit_dynamic():
    '''
    This function displays all of the associated view/actions for editing a dynamic scholarship
    and overwriting the old version with the new version in the scholarship file.
    '''
    edit_sch = st.selectbox("Select the scholarship to edit", options=scholarships['Name'])
    if button('Edit This Scholarship', key='Edit This Scholarship'):
        # Don't let them try to edit nothing.
        if edit_sch is None:
            st.write('There is no scholarship selected')
        else:
            # values is the current values of the scholarship, index is the row of that scholarship
            # Find both the index and the values that match the scholarship we are trying to edit.
            for ind in range(0, scholarships.shape[0]):
                values = scholarships.iloc[ind]
                if values['Name'] == edit_sch:
                    index = ind
                    break
            # Every time a value is selected in the criteria multiselect it gets a display
            dyn_columns = st.multiselect("Choose criteria to edit", options=SCH_COLUMNS, help='''Every criteria you select
                                        will create a field with the current value prepopulated. If there is currently no value,
                                        it will render with no value in it.''')
            for col in dyn_columns:
                # Groups need a multiselect so they are checked for by name as they are hardset to have "Group" at the beginning.
                # Its necessary to check if the value is nan as it will error if you try to pass nan into default
                if col[0:5] == "Group" and not pd.isnull(values[col]):
                    chosen_val = st.multiselect('Edit ' + col, options=GROUP_OPTIONS, default=groups_string_to_list(values[col]), help=GROUP_HELP)
                    chosen_val = str(chosen_val)
                elif col[0:5] == "Group":
                    chosen_val = st.multiselect('Edit ' + col, options=GROUP_OPTIONS, help=GROUP_HELP)
                    chosen_val = str(chosen_val)
                # This case handles all other values that aren't groups
                else:
                # This is so that nan is not displayed in the fields when there is no value and it is instead blank
                    if not pd.isnull(values[col]):
                        chosen_val = st.text_input('Edit ' + col, value=values[col])
                    else:
                        chosen_val = st.text_input('Edit ' + col)
                    # Edit the row with the new value
                edit_row(scholarships, index, [(col, chosen_val)])
            if st.button('Finalize Changes', key='Finalize Changes'):
                # We changed the values in our scholarships dataframe, but have not updated the actual file, so that is done here
                write_rows(scholarships, 'data/Scholarships.xlsx', 'Scholarships', creds)
                st.write(edit_sch + " has been successfully edited.")


def display_delete():
    """
    This function displays all the associated view/actions for deleting a scholarship
    and removing it from the scholarship file.
    """
    delete_sch = st.selectbox("Select the scholarship to delete", options=st.session_state.scholarships['Name'])
    if button('Delete This Scholarship', key='Delete This Scholarship'):
        # Don't let them try to delete nothing.
        if delete_sch is None:
            st.write('There is no scholarship selected')
        else:
            st.write('Are you sure you want to delete this scholarship? It cannot be undone after.')
            # Extra layers of decisions to make sure they want to do this.
            if st.button('Finalize Deletion', key='Finalize Deletion'):
                # index is the row index of the scholarship we are deleting.
                for ind in range(0, st.session_state.scholarships.shape[0]):
                    values = st.session_state.scholarships.iloc[ind]
                    if values['Name'] == delete_sch:
                        index = ind
                        break
                # In this case, drop takes the row index and drops the associated row, returning a new dataframe
                # without it.
                new_scholarships = st.session_state.scholarships.drop(index=index)
                # We deleted the scholarship in our scholarships dataframe, but have not updated the actual file,
                # so that is done here.
                write_rows(new_scholarships, 'data/Scholarships.xlsx', 'Scholarships', creds)
                st.session_state.scholarships = new_scholarships
                st.write(delete_sch + ' has been successfully deleted.')


def display_import():
    """
    This function displays all the associated view/actions for importing scholarships
    from outside files and either overwriting or adding to the previous scholarships file
    """
    st.title("Import Scholarships")
    form = st.form(key="scholarship_import_form")
    file = form.file_uploader('Scholarship Source:', accept_multiple_files=True, type=[
        'xlsx', 'csv', 'tsv'])
    form.markdown(centered_text(
        '<em>supports both excel and csv format</em>'), unsafe_allow_html=True)

    submit_new = form.form_submit_button('Import Scholarships as New', help="""Warning: Please make sure column names
    and values are consistent with the values of a normally created scholarship through the application or else 
    unintended errors can happen.""")
    submit_add = form.form_submit_button('Import Scholarships to Existing', help="""Warning: Please make sure column
    names and values are consistent with the values of a normally created scholarship through the application or else 
    unintended errors can happen.""")

    columns = ['Name', 'Total Amount', 'Value', 'RAI', 'Admit Score', 'Major', 'ACT Math', 'ACT English',
               'ACT Composite',
               'SAT Math', 'SAT Reading', 'SAT Combined', 'GPA', 'HS Percentile', 'Group One', 'Group Two',
               'Group Three']

    if submit_new:
        # Handle imported files.
        if not file:
            st.write('No file selected!')
            return
        # Do not want them to try and create a new file with two separate ones
        if len(file) > 1:
            st.write('Only select one file.')
            return

        new_scholarships = read_rows(file[0], creds)
        # Validation checking to make sure that all the columns are the same
        new_columns = new_scholarships.columns
        fail_columns, invalid_columns, missing_columns = check_columns_equal(columns, new_columns)
        for col in invalid_columns:
            st.write(col + " column is not a valid column.")
        for col in missing_columns:
            st.write(col + " column is missing.")
        # Succeed if there are no failures
        if fail_columns == 0:
            write_rows(new_scholarships, 'data/Scholarships.xlsx', 'Scholarships', creds)
            st.write(file[0].name + " has been successfully imported as your new scholarships.")

    if submit_add:
        # Handle imported files.
        if not file:
            st.write('No files selected!')
            return
        # This is not necessary technically, but it could be confusing since it is necessary for new
        # The ability to add in more than one at a time is possible, but really not a priority or necessary.
        if len(file) > 1:
            st.write('Only select one file.')
            return

        add_scholarships = read_rows(file[0], creds)
        old_scholarships = scholarships
        # Validation checking to make sure that all the columns are the same
        add_columns = add_scholarships.columns
        fail_columns, invalid_columns, missing_columns = check_columns_equal(columns, add_columns)
        for col in invalid_columns:
            st.write(col + " column is not a valid column.")
        for col in missing_columns:
            st.write(col + " column is missing.")
        # Succeed if there are no failures
        if fail_columns == 0:
            for _, row in add_scholarships.iterrows():
                old_scholarships = old_scholarships.append(row)
            write_rows(old_scholarships, 'data/Scholarships.xlsx', 'Scholarships', creds)
            st.write(file[0].name + " has been successfully added to the existing scholarships.")


st.title("Scholarship Management")
st.write("Select an Action from Below")

with st.container():
    if button('Create New Scholarship', key='Create New Dynamic Scholarship'):
        display_create_dynamic()
    elif button('Edit Existing Scholarship', key='Edit Existing Scholarship'):
        display_edit_dynamic()
    elif button('Delete Existing Scholarship', key='Delete Existing Scholarship'):
        display_delete()

display_import()
