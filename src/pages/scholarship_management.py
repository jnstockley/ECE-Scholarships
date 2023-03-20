'''
scholarship managment page render
'''
import streamlit as st
from streamlit_extras.stateful_button import button

st.title("Scholarship Management")
st.write("Select an Action from Below")

with st.container():
    if button('Create New Scholarship', key='Create New Scholarship'):
        st.title('Create a new scholarship')
        #Note: text_input is used instead of number_input because I feel like the stepping functionality is unnecessary and could
        #throw them off when they see it or they could accidentally hit it. This can be changed later if it is found useful.
        st.text_input("Amount of Scholarships", max_chars=8, placeholder="Enter Numerical Amount")
        st.text_input('The value of each individual Scholarship', max_chars=8, placeholder="Enter Numerical Amount")
        st.write('What are the criteria of the scholarship?')
    if button('Edit Existing Scholarship', key='Edit Existing Scholarship'):
        st.write('form for editing')
    if button('Delete Existing Scholarship', key='Delete Existing Scholarship'):
        st.write('form for deleting')

#if button("Button 1", key="button1"):
#if button("Button 2", key="button2"):
#if button("Button 3", key="button3"):
