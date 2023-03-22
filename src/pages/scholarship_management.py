'''
scholarship managment page render
'''
import streamlit as st
from streamlit_extras.stateful_button import button
import pandas as pd

# if 'scholarships' not in st.session_state:
#     st.session_state['scholarships'] = {}
# if 'scholarship_names' not in st.session_state:
#     st.session_state['scholarship_names'] = []

scholarships_excel = pd.read_excel('./scholarships/scholarships.xlsx')
scholarships = scholarships_excel.head()
#NOTE: Here for viewing purposes
#print(scholarships)
#print(scholarships.shape[0])

#NOTE: Uncomment these two lines if you want to reset the scholarships.xlsx file to the single entry below. You must comment it back out
#after you run it once or it will continuously reset it.
#df = pd.DataFrame({'Name':['Test One'], 'Total Amount':['1000'], 'Value':['8000'], 'Major':['All'], 'ACT':['26'], 'SAT Math': ['600'], 'SAT Reading': ['400'], 'SAT Combined':['1000'], 'GPA':['4.0']})
#df.to_excel('./scholarships/scholarships.xlsx', sheet_name='Scholarships', index=False)

st.title("Scholarship Management")
st.write("Select an Action from Below")

with st.container():
    majors = ["Computer Science and Engineering", "Electrical Engineering", "All"]
    if button('Create New Scholarship', key='Create New Scholarship'):
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
        sat_math = st.select_slider('New minimum SAT Math requirement', options=(x*10 for x in range(0,81)))
        sat_reading = st.select_slider('New minimum SAT Reading requirement', options=(x*10 for x in range(0,81)))
        sat_comb = st.select_slider('Select the minimum SAT Combined requirement', options=(x*10 for x in range(0,161)))
        gpa = st.select_slider('Select the minimum GPA requirement', options=(x/20 for x in range (0,101)))
        if st.button('Create'):
            if name == "" or total == "" or value == "":
                st.write("Please make sure all the fields are filled out.")
            else:
                scholarship = pd.Series(data=[name, total, value, major, act, sat_math, sat_reading, sat_comb, gpa], index=scholarships.columns, name = scholarships.shape[0])
                new_scholarships = scholarships.append(scholarship)
                new_scholarships.to_excel('./scholarships/scholarships.xlsx', sheet_name='Scholarships', index=False)
                st.write(name + " has been successfully created.")

    elif button('Edit Existing Scholarship', key='Edit Existing Scholarship'):
        edit_sch = st.selectbox("Select the scholarship to edit", options=scholarships['Name'])
        if button('Edit This Scholarship', key = 'Edit This Scholarship'):
            if edit_sch is None:
                st.write('There is no scholarship selected')
            else:
                values = None
                index = None
                for n in range(0, scholarships.shape[0]):
                    values = scholarships.iloc[n]
                    if values['Name'] == edit_sch:
                        index = n
                        break    
                total = st.text_input("New total amount of Scholarships", value = values['Total Amount'], max_chars=8, placeholder="Enter Numerical Amount")
                value = st.text_input('New value of each individual Scholarship', value = values['Value'], max_chars=8, placeholder="Enter Numerical Amount")
                major = st.selectbox("New majors the scholarship applies to", index = majors.index(values['Major']), options=majors)
                act = st.select_slider('New minimum ACT requirement', value=values['ACT'], options=range(1,37))
                sat_math = st.select_slider('New minimum SAT Math requirement', value=values['SAT Math'], options=(x*10 for x in range(0,81)))
                sat_reading = st.select_slider('New minimum SAT Reading requirement', value=values['SAT Reading'], options=(x*10 for x in range(0,81)))
                sat_comb = st.select_slider('Select the minimum SAT Combined requirement', value=values['SAT Combined'], options=(x*10 for x in range(0,161)))
                gpa = st.select_slider('New minimum GPA requirement', value=values['GPA'], options=(x/20 for x in range (0,101)))
                if st.button('Finalize Changes'):
                    scholarships.loc[index, 'Total Amount'] = total
                    scholarships.loc[index, 'Value'] = value
                    scholarships.loc[index, 'Major'] = major
                    scholarships.loc[index, 'ACT'] = act
                    scholarships.loc[index, 'SAT Math'] = sat_math
                    scholarships.loc[index, 'SAT Reading'] = sat_reading
                    scholarships.loc[index, 'SAT Combined'] = sat_comb
                    scholarships.loc[index, 'GPA'] = gpa
                    scholarships.to_excel('./scholarships/scholarships.xlsx', sheet_name='Scholarships', index=False)
                    st.write(edit_sch + " has been successfully edited.")

    elif button('Delete Existing Scholarship', key='Delete Existing Scholarship'):
        delete_sch = st.selectbox("Select the scholarship to delete", options=scholarships['Name'])
        if button ('Delete This Scholarship', key='Delete This Scholarship'):
            if delete_sch is None:
                st.write('There is no scholarship selected')
            else:
                st.write('Are you sure you want to delete this scholarship?')
                if st.button('Finalize Deletion'):
                    index = None
                    for n in range(0, scholarships.shape[0]):
                        values = scholarships.iloc[n]
                        if values['Name'] == delete_sch:
                            index = n
                            break 
                    new_scholarships = scholarships.drop(index=index)
                    new_scholarships.to_excel('./scholarships/scholarships.xlsx', sheet_name='Scholarships', index=False)
                    st.write(delete_sch + ' has been successfully deleted.')
                    st.session_state['finalize_disabled'] = True


#Note: might need to define functions so that state information can be used differently? Not sure, but as of now I can only disable buttons that come
#ahead of the buttons being disabled which isnt a big deal so save this for last
#Note: can edit the visibility using session state variables for a cleaner looking application. See above
