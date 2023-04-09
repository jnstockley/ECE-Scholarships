'''
scholarship managment page render
'''
import streamlit as st
from streamlit_extras.stateful_button import button
import pandas as pd
from src.utils.html import centered_text
# from src.utils.output import get_output_dir

# This first reads the excel spreadsheet at the file destination and then places the rows in scholarships
# NOTE: This needs to be changed once sharepoint is implemented to read from there instead of locally.
# scholarships_excel = pd.read_excel('.app_data/scholarships/scholarships.xlsx')
scholarships_excel = pd.read_excel('tests/data/scholarships.xlsx')
scholarships = scholarships_excel.head()

st.title("Scholarship Management")
st.write("Select an Action from Below")

# Global variables; majors contains all the majors, group options is all the column names that can be selected for a group
# and group help is the help message when hovering over the ? on a group field.
MAJORS = ['Computer Science and Engineering', 'Electrical Engineering', 'All']
GROUP_OPTIONS = ['RAI', 'Admit Score', 'Major', 'ACT Math', 'ACT English', 'ACT Composite',
                    'SAT Math', 'SAT Reading', 'SAT Combined', 'GPA', 'HS Percentile'] 
GROUP_HELP="""A requirement grouping groups the selected requirements so only one is required.
            i.e. ACT Composite, SAT Combined, HS Percentile all being selected requires only the 
            minimum requirement of ACT Composite, SAT Combined, or HS Percentile."""

def groups_string_to_list(default_options):
    '''
    This function is for converting the groups read in from the pandas dataframe ('Group One', etc.) from a string
    to the original list they were. Example: ['ACT Composite', 'SAT Combined'] is converted to "['ACT Composite', 'SAT Combined']"
    when the data is read it, this function converts it back to ['ACT Composite', 'SAT Combined'].
    '''
    # Needed edge case for when there is no options
    if default_options == "[]":
        return []
    # Removes [] from the string
    no_brackets = default_options[1:(len(default_options)-1)]
    # Removes ' ' around the items in the group
    no_quotes = no_brackets.replace('\'', '')
    # Removes the ,_ from the string and places everything into the split list
    list_form = no_quotes.split(', ')
    return list_form

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
            # We rewrite the file with the new_scholarships dataframe, which has the new scholarship in it.
            # NOTE: This needs to be changed with sharepoint to save there instead of locally.
            new_scholarships.to_excel('tests/data/scholarships.xlsx', sheet_name='Scholarships', index=False)
            # new_scholarships.to_excel(f"{get_output_dir('scholarships')}/scholarships.xlsx", sheet_name='Scholarships', index=False)
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
                # loc takes in the row index and the column name and rewrites the value of that row and column
                scholarships.loc[index, 'Total Amount'] = total
                scholarships.loc[index, 'Value'] = value
                scholarships.loc[index, 'RAI'] = rai
                scholarships.loc[index, 'Admit Score'] = admit_score
                scholarships.loc[index, 'Major'] = major
                scholarships.loc[index, 'ACT Math'] = act_math
                scholarships.loc[index, 'ACT English'] = act_english
                scholarships.loc[index, 'ACT Composite'] = act_comp
                scholarships.loc[index, 'SAT Math'] = sat_math
                scholarships.loc[index, 'SAT Reading'] = sat_reading
                scholarships.loc[index, 'SAT Combined'] = sat_comb
                scholarships.loc[index, 'GPA'] = gpa
                scholarships.loc[index, 'HS Percentile'] = hs_percentile
                scholarships.loc[index, 'Group One'] = str(group1)
                scholarships.loc[index, 'Group Two'] = str(group2)
                scholarships.loc[index, 'Group Three'] = str(group3)
                # We changed the values in our scholarships dataframe, but have not updated the actual file, so that is done here
                # NOTE: This needs to be changed with sharepoint to save there instead of locally.
                scholarships.to_excel('tests/data/scholarships.xlsx', sheet_name='Scholarships', index=False)
                # scholarships.to_excel(f"{get_output_dir('scholarships')}/scholarships.xlsx", sheet_name='Scholarships', index=False)
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
                # NOTE: This needs to be changed with sharepoint to save there instead of locally.
                new_scholarships.to_excel('tests/data/scholarships.xlsx', sheet_name='Scholarships', index=False)
                # new_scholarships.to_excel(f"{get_output_dir('scholarships')}/scholarships.xlsx", sheet_name='Scholarships', index=False)
                st.write(delete_sch + ' has been successfully deleted.')

with st.container():
    if button('Create New Scholarship', key='Create New Scholarship'):
        display_create()
    elif button('Edit Existing Scholarship', key='Edit Existing Scholarship'):
        display_edit()
    elif button('Delete Existing Scholarship', key='Delete Existing Scholarship'):
        display_delete()


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

        new_scholarships_excel = pd.read_excel(file[0])
        new_scholarships = new_scholarships_excel.head()
        # Validation checking to make sure that all the columns are the same
        new_columns = new_scholarships.columns
        fail_columns = 0
        # Check to make sure that there are no extra/different columns
        for col in new_columns:
            if col not in columns:
                st.write(col + " column is not a valid column.")
                fail_columns += 1
        # Check to make sure that there are no missing columns
        for col in columns:
            if col not in new_columns:
                st.write(col + " column is missing.")
                fail_columns += 1
        # Succeed if there are no failures
        if fail_columns == 0:
            new_scholarships.to_excel('tests/data/scholarships.xlsx', sheet_name='Scholarships', index=False)
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

        add_scholarships_excel = pd.read_excel(file[0])
        add_scholarships = add_scholarships_excel.head()
        old_scholarships = scholarships
        # Validation checking to make sure that all the columns are the same
        add_columns = add_scholarships.columns
        fail_columns = 0
        # Check to make sure that there are no extra/different columns
        for col in add_columns:
            if col not in columns:
                st.write(col + " column is not a valid column.")
                fail_columns += 1
        # Check to make sure that there are no missing columns
        for col in columns:
            if col not in add_columns:
                st.write(col + " column is missing.")
                fail_columns += 1
        # Succeed if there are no failures
        if fail_columns == 0:
            for _, row in add_scholarships.iterrows():
                old_scholarships = old_scholarships.append(row)
            old_scholarships.to_excel('tests/data/scholarships.xlsx', sheet_name='Scholarships', index=False)
            st.write(file[0].name + " has been successfully added to the existing scholarships.")

display_import()
