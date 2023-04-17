'''
scholarship managment page render
'''
import streamlit as st
from streamlit_extras.stateful_button import button
import pandas as pd
from src.utils.html import centered_text
from src.utils.scholarship_management import read_rows, write_rows, edit_row, groups_string_to_list, check_columns_equal

if 'n_groups' not in st.session_state:
    st.session_state.n_groups = 1

# Global variables; majors contains all the majors, group options is all the column names that can be selected for a group
# and group help is the help message when hovering over the ? on a group field.
SCH_COLUMNS = ['ACT Math', 'ACT English', 'Random1']
MAJORS = ['Computer Science and Engineering', 'Electrical Engineering', 'All']
GROUP_OPTIONS = ['RAI', 'Admit Score', 'Major', 'ACT Math', 'ACT English', 'ACT Composite',
                    'SAT Math', 'SAT Reading', 'SAT Combined', 'GPA', 'HS Percentile'] 
GROUP_HELP="""A requirement grouping groups the selected requirements so only one is required.
            i.e. ACT Composite, SAT Combined, HS Percentile all being selected requires only the 
            minimum requirement of ACT Composite, SAT Combined, or HS Percentile."""

scholarships = read_rows('tests/data/scholarships.xlsx')


def display_create_dynamic():
    st.title('Create a New Scholarship')
    dyn_columns = st.multiselect("Choose Relevant Columns to this scholarship", options=SCH_COLUMNS, help='Placeholder')
    col_values = {}
    for val in dyn_columns:
        chosenVal = st.select_slider('Select the minimum ' + val + ' requirement', options=range(0,37))
        col_values[val] = chosenVal
    group_count = 0
    if st.button('Add a Requirement Grouping', key='Add a Requirement Grouping'):
        st.session_state.n_groups += 1
        st.experimental_rerun()
    for i in range(st.session_state.n_groups):
        group = st.multiselect("Choose Group " + str(i), options=GROUP_OPTIONS, help=GROUP_HELP)
    print(col_values)


def display_create():
    '''
    This function displays all of the associated view/actions for creating a scholarship
    and adding it to the scholarship file.
    '''
    st.title('Create a New Scholarship')
    st.write('If certain requirements are N/A, leave them at 0.')
    # NOTE: text_input is used instead of number_input because I feel like the stepping functionality is unnecessary and could
    # throw them off when they see it or they could accidentally hit it. This can be changed later if it is found useful.
    name = st.text_input("Scholarship Name", max_chars=500, placeholder="Enter Scholarship Name")
    total = st.text_input("Total amount of Scholarships", max_chars=8, placeholder="Enter Numerical Amount")
    value = st.text_input('The value of each individual Scholarship', max_chars=8, placeholder="Enter Numerical Amount")
    # NOTE: I chose up to 400 for the RAI, but the highest value in the sample data is 363, I am not sure if RAI has a hard max score.
    rai = st.select_slider('Select the minimum RAI requirement', options=(x*5 for x in range(0,81)))
    # NOTE: I chose up to 36 for this as that is the max in the sample data.
    admit_score = st.select_slider('Select the minimum Admit Score requirement', options=range(0,37))
    major = st.selectbox("Select which majors the scholarship applies to", options=MAJORS)
    act_math = st.select_slider('Select the minimum ACT Math requirement', options=range(0,37))
    act_english = st.select_slider('Select the minimum ACT English requirement', options=range(0,37))
    act_comp = st.select_slider('Select the minimum ACT Composite requirement', options=range(0,37))
    sat_math = st.select_slider('New minimum SAT Math requirement', options=(x*10 for x in range(0,81)))
    sat_reading = st.select_slider('New minimum SAT Reading requirement', options=(x*10 for x in range(0,81)))
    sat_comb = st.select_slider('Select the minimum SAT Combined requirement', value=(sat_math + sat_reading), options=(x*10 for x in range(0,161)))
    # NOTE: 5.0 was chosen as the max for the GPA requirement, but there exists a couple students above 5.0. This could be increased if necessarily,
    # but I doubt any scholarships require above 5.0, or even above 4.0, as that would greatly limit students unfairly.
    gpa = st.select_slider('Select the minimum GPA requirement', options=(x/20 for x in range (0,101)))
    hs_percentile = st.select_slider('Select the minimum highschool percentile', options=(x for x in range(0,101)))

    group1 = []
    group2 = []
    group3 = []
    if button('Add a Requirement Grouping', key='Add a Requirement Grouping'):
        group1 = st.multiselect("Choose Group One", options=GROUP_OPTIONS, help=GROUP_HELP)
        if button('Add a second Requirement Grouping', key='Add a second Requirement Grouping'):
            group2 = st.multiselect("Choose Group Two", options=GROUP_OPTIONS, help=GROUP_HELP)
            if button('Add a third Requirement Grouping', key='Add a third Requirement Grouping'):
                group3 = st.multiselect("Choose Group Three", options=GROUP_OPTIONS, help=GROUP_HELP)
    if st.button('Create Scholarship', key='Create Scholarship'):
        # These fields should not be able to be blank
        if name == "" or total == "" or value == "":
            st.write("Please make sure all the fields are filled out.")
        else:
            # pd.Series creates a Panda object that can be appended to the scholarships dataframe.
            scholarship = pd.Series(data=[name, total, value, rai, admit_score, major, act_math, act_english, act_comp, sat_math, sat_reading,
                                            sat_comb, gpa, hs_percentile, group1, group2, group3],
                                        index=scholarships.columns, name = scholarships.shape[0])
            new_scholarships = scholarships.append(scholarship)
            write_rows(new_scholarships, 'tests/data/scholarships.xlsx', 'Scholarships')
            st.write(name + " has been successfully created.")

def display_edit():
    '''
    This function displays all of the associated view/actions for editing a scholarship
    and overwriting the old version with the new version in the scholarship file.
    '''
    edit_sch = st.selectbox("Select the scholarship to edit", options=scholarships['Name'])
    if button('Edit This Scholarship', key = 'Edit This Scholarship'):
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
            # Display the information; value is set so that it loads the current values into the fields.
            total = st.text_input("New total amount of Scholarships", value = values['Total Amount'], max_chars=8, placeholder="Enter Numerical Amount")
            value = st.text_input('New value of each individual Scholarship', value = values['Value'], max_chars=8, placeholder="Enter Numerical Amount")
            rai = st.select_slider('Select the minimum RAI requirement', value=values['RAI'], options=(x*5 for x in range(0,81)))
            admit_score = st.select_slider('Select the minimum Admit Score requirement', value=values['Admit Score'], options=range(0,37))
            major = st.selectbox("New majors the scholarship applies to", index = MAJORS.index(values['Major']), options=MAJORS)
            act_math = st.select_slider('Select the minimum ACT Math requirement', value=values['ACT Math'], options=range(0,37))
            act_english = st.select_slider('Select the minimum ACT English requirement', value=values['ACT English'], options=range(0,37))
            act_comp = st.select_slider('New minimum ACT Composite requirement', value=values['ACT Composite'], options=range(0,37))
            sat_math = st.select_slider('New minimum SAT Math requirement', value=values['SAT Math'], options=(x*10 for x in range(0,81)))
            sat_reading = st.select_slider('New minimum SAT Reading requirement', value=values['SAT Reading'], options=(x*10 for x in range(0,81)))
            sat_comb = st.select_slider('Select the minimum SAT Combined requirement', value=values['SAT Combined'], options=(x*10 for x in range(0,161)))
            gpa = st.select_slider('New minimum GPA requirement', value=values['GPA'], options=(x/20 for x in range (0,101)))
            hs_percentile = st.select_slider('Select the minimum highschool percentile', value=values['HS Percentile'], options=(x for x in range(0,101)))
            group1 = st.multiselect("Choose Group One", options=GROUP_OPTIONS, default=groups_string_to_list(values['Group One']), help=GROUP_HELP)
            group2 = st.multiselect("Choose Group Two", options=GROUP_OPTIONS, default=groups_string_to_list(values['Group Two']), help=GROUP_HELP)
            group3 = st.multiselect("Choose Group Three", options=GROUP_OPTIONS, default=groups_string_to_list(values['Group Three']), help=GROUP_HELP)
            if st.button('Finalize Changes', key='Finalize Changes'):
                edit_row(scholarships, index, [('Total Amount', total), ('Value', value), ('RAI', rai), ('Admit Score', admit_score),('Major', major),
                                               ('ACT Math', act_math), ('ACT English', act_english), ('ACT Composite', act_comp),('SAT Math', sat_math),
                                               ('SAT Reading', sat_reading), ('SAT Combined', sat_comb), ('GPA', gpa),('HS Percentile', hs_percentile),
                                               ('Group One', str(group1)), ('Group Two', str(group2)), ('Group Three', str(group3))])
                # We changed the values in our scholarships dataframe, but have not updated the actual file, so that is done here
                write_rows(scholarships, 'tests/data/scholarships.xlsx', 'Scholarships')
                st.write(edit_sch + " has been successfully edited.")

def display_delete():
    '''
    This function displays all of the associated view/actions for deleting a scholarship
    and removing it from the scholarship file.
    '''
    delete_sch = st.selectbox("Select the scholarship to delete", options=scholarships['Name'])
    if button ('Delete This Scholarship', key='Delete This Scholarship'):
        # Don't let them try to delete nothing.
        if delete_sch is None:
            st.write('There is no scholarship selected')
        else:
            st.write('Are you sure you want to delete this scholarship? It cannot be undone after.')
            # Extra layers of decisions to make sure they want to do this.
            if st.button('Finalize Deletion', key='Finalize Deletion'):
                # index is the row index of the scholarship we are deleting.
                for ind in range(0, scholarships.shape[0]):
                    values = scholarships.iloc[ind]
                    if values['Name'] == delete_sch:
                        index = ind
                        break
                # In this case, drop takes the row index and drops the associated row, returning a new dataframe without it.
                new_scholarships = scholarships.drop(index=index)
                # We deleted the scholarship in our scholarships dataframe, but have not updated the actual file, so that is done here.
                write_rows(new_scholarships, 'tests/data/scholarships.xlsx', 'Scholarships')
                st.write(delete_sch + ' has been successfully deleted.')

def display_import():
    '''
    This function displays all of the associated view/actions for importing scholarships
    from outside files and either overwriting or adding to the previous scholarships file
    '''
    st.title("Import Scholarships")
    form = st.form(key="scholarship_import_form")
    file = form.file_uploader('Scholarship Source:', accept_multiple_files=True, type=[
                               'xlsx', 'csv', 'tsv'])
    form.markdown(centered_text(
        '<em>supports both excel and csv format</em>'), unsafe_allow_html=True)

    submit_new = form.form_submit_button('Import Scholarships as New', help="""Warning: Please make sure column names and values are consistent
                                                                            with the values of a normally created scholarship through the application
                                                                            or else unintended errors can happen.""")
    submit_add = form.form_submit_button('Import Scholarships to Existing', help="""Warning: Please make sure column names and values are consistent
                                                                            with the values of a normally created scholarship through the application
                                                                            or else unintended errors can happen.""")

    columns = ['Name', 'Total Amount', 'Value', 'RAI', 'Admit Score', 'Major', 'ACT Math', 'ACT English','ACT Composite',
               'SAT Math', 'SAT Reading', 'SAT Combined', 'GPA', 'HS Percentile', 'Group One', 'Group Two', 'Group Three']

    if submit_new:
        # Handle imported files.
        if not file:
            st.write('No file selected!')
            return
        # Do not want them to try and create a new file with two separate ones
        if len(file) > 1:
            st.write('Only select one file.')
            return

        new_scholarships = read_rows(file[0])
        # Validation checking to make sure that all the columns are the same
        new_columns = new_scholarships.columns
        fail_columns, invalid_columns, missing_columns = check_columns_equal(columns, new_columns)
        for col in invalid_columns:
            st.write(col + " column is not a valid column.")
        for col in missing_columns:
            st.write(col + " column is missing.")
        # Succeed if there are no failures
        if fail_columns == 0:
            write_rows(new_scholarships, 'tests/data/scholarships.xlsx', 'Scholarships')
            st.write(file[0].name + " has been successfully imported as your new scholarships.")

    if submit_add:
        # Handle imported files.
        if not file:
            st.write('No files selected!')
            return
        # This is not necessary technically but it could be confusing since it is necessary for new
        # The ability to add in more than one at a time is possible, but really not a priority or necessary.
        if len(file) > 1:
            st.write('Only select one file.')
            return

        add_scholarships = read_rows(file[0])
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
            write_rows(old_scholarships, 'tests/data/scholarships.xlsx', 'Scholarships')
            st.write(file[0].name + " has been successfully added to the existing scholarships.")

st.title("Scholarship Management")
st.write("Select an Action from Below")

with st.container():
    if button('Create New Dynamic Scholarship', key='Create New Dynamic Scholarship'):
        display_create_dynamic()
    if button('Create New Scholarship', key='Create New Scholarship'):
        display_create()
    elif button('Edit Existing Scholarship', key='Edit Existing Scholarship'):
        display_edit()
    elif button('Delete Existing Scholarship', key='Delete Existing Scholarship'):
        display_delete()

display_import()
