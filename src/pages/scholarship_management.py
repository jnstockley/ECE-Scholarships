'''
scholarship managment page render
'''
import streamlit as st
from streamlit_extras.stateful_button import button
import numpy as np

st.title("Scholarship Management")
st.write("Select an Action from Below")

with st.container():
    if button('Create New Scholarship', key='Create New Scholarship'):
        st.title('Create a new scholarship')
        #Note: text_input is used instead of number_input because I feel like the stepping functionality is unnecessary and could
        #throw them off when they see it or they could accidentally hit it. This can be changed later if it is found useful.
        total = st.text_input("Total amount of Scholarships", max_chars=8, placeholder="Enter Numerical Amount")
        value = st.text_input('The value of each individual Scholarship', max_chars=8, placeholder="Enter Numerical Amount")
        act = st.select_slider('Select the minimum ACT requirement', options=range(1,37))
        major = st.selectbox("Select which majors the scholarship applies to", options=["Computer Science and Engineering", "Electrical Engineering", "N/A"])
        gpa = st.select_slider('Select the minimum GPA requirement', options=(x/5 for x in range (0,51)))
    if button('Edit Existing Scholarship', key='Edit Existing Scholarship'):
        st.write('form for editing')
    if button('Delete Existing Scholarship', key='Delete Existing Scholarship'):
        st.write('form for deleting')
