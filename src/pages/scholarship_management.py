'''
scholarship managment page render
'''
import streamlit as st
from streamlit_extras.stateful_button import button
import pandas as pd

if 'scholarships' not in st.session_state:
    st.session_state['scholarships'] = {}
if 'scholarship_names' not in st.session_state:
    st.session_state['scholarship_names'] = []
if 'create_vis' not in st.session_state:
    st.session_state['create_disabled'] = False
if 'edit_vis' not in st.session_state:
    st.session_state['edit_disabled'] = False
if 'delete_vis' not in st.session_state:
    st.session_state['delete_disabled'] = False

scholarships_excel = pd.read_excel('./scholarships/scholarships.xlsx')
scholarships = scholarships_excel.head()
#NOTE: Here for viewing purposes
#print(scholarships)
#print(scholarships.shape[0])

#NOTE: Uncomment these two lines if you want to reset the scholarships.xlsx file to the single entry below. You must comment it back out
#after you run it once or it will continuously reset it.
#df = pd.DataFrame({'Name':['Test One'], 'Total Amount':[1000], 'Value':[8000], 'Major':['N/A'], 'ACT':[26], 'SAT':[1000], 'GPA':[3.25]})
#df.to_excel('./scholarships/scholarships.xlsx', sheet_name='Scholarships', index=False)

st.title("Scholarship Management")
st.write("Select an Action from Below")

with st.container():
    majors = ["Computer Science and Engineering", "Electrical Engineering", "N/A"]
    if button('Create New Scholarship', disabled=st.session_state["create_disabled"], key='Create New Scholarship'):
        st.title('Create a new scholarship')
        st.session_state["edit_disabled"] = True
        st.session_state['delete_disabled'] = True
        #NOTE: text_input is used instead of number_input because I feel like the stepping functionality is unnecessary and could
        #throw them off when they see it or they could accidentally hit it. This can be changed later if it is found useful.
        name = st.text_input("Scholarship Name", max_chars=500, placeholder="Enter Scholarship Name")
        total = st.text_input("Total amount of Scholarships", max_chars=8, placeholder="Enter Numerical Amount")
        value = st.text_input('The value of each individual Scholarship', max_chars=8, placeholder="Enter Numerical Amount")
        major = st.selectbox("Select which majors the scholarship applies to", options=majors)
        act = st.select_slider('Select the minimum ACT requirement', options=range(0,37))
        sat = st.select_slider('Select the minimum SAT requirement', options=(x*10 for x in range(0,161)))
        gpa = st.select_slider('Select the minimum GPA requirement', options=(x/5 for x in range (0,26)))
        if st.button('Create'):
            if name == "" or total == "" or value == "":
                st.write("Please make sure all the fields are filled out.")
            else:
                scholarship = pd.Series(data=[name, total, value, major, act, sat, gpa], index=scholarships.columns, name = scholarships.shape[0])
                new_scholarships = scholarships.append(scholarship)
                new_scholarships.to_excel('./scholarships/scholarships.xlsx', sheet_name='Scholarships', index=False)
                scholarship_values = {'total': int(total), 'value': int(value), 'major': major, 'act': int(act), 'sat': int(sat), 'gpa': float(gpa)}
                st.session_state["scholarships"][name] = scholarship_values
                st.session_state["scholarship_names"].append(name)
                st.write(name + " has been successfully created.")

    if button('Edit Existing Scholarship', disabled=st.session_state["edit_disabled"], key='Edit Existing Scholarship'):
        edit_sch = st.selectbox("Select the scholarship to edit", options=st.session_state['scholarship_names'])
        st.session_state['create_disabled'] = True
        st.session_state['delete_disabled'] = True
        if button('Edit This Scholarship', key = 'Edit This Scholarship'):
            if edit_sch is None:
                st.write('There is no scholarship selected')
            else:
                name = edit_sch
                values = st.session_state["scholarships"][name]
                total = st.text_input("New total amount of Scholarships", value = values['total'], max_chars=8, placeholder="Enter Numerical Amount")
                value = st.text_input('New value of each individual Scholarship', value = values['value'], max_chars=8, placeholder="Enter Numerical Amount")
                major = st.selectbox("New majors the scholarship applies to", index = majors.index(values['major']), options=["Computer Science and Engineering", "Electrical Engineering", "N/A"])
                act = st.select_slider('New minimum ACT requirement', value=values['act'], options=range(1,37))
                sat = st.select_slider('New minimum SAT requirement', value=values['sat'], options=(x*10 for x in range(0,161)))
                gpa = st.select_slider('New minimum GPA requirement', value=values['gpa'], options=(x/5 for x in range (0,51)))
                if button('Finalize Changes', key = 'Finalize Changes'):
                    newValues = {'total': total, 'value': value, 'major': major, 'act': act, 'sat': sat, 'gpa': gpa}
                    st.session_state["scholarships"][name] = newValues

    if button('Delete Existing Scholarship', disabled=st.session_state["delete_disabled"], key='Delete Existing Scholarship'):
        delete_sch = st.selectbox("Select the scholarship to delete", options=st.session_state['scholarship_names'])
        if button ('Delete This Scholarship', key='Delete This Scholarship'):
            st.session_state['create_disabled'] = True
            st.session_state['edit_disabled'] = True
            if delete_sch is None:
                st.write('There is no scholarship selected')
            else:
                st.write('Are you sure you want to delete this scholarship?')
                if button ('Finalize Deletion', key='Finalize Deletion'):
                    del st.session_state['scholarships'][delete_sch]
                    st.session_state['scholarship_names'].remove(delete_sch)
                    st.write(delete_sch + ' has been successfully deleted.')

#Note: might need to define functions so that state information can be used differently? Not sure, but as of now I can only disable buttons that come
#ahead of the buttons being disabled which isnt a big deal so save this for last
#Note: can edit the visibility using session state variables for a cleaner looking application. See above
