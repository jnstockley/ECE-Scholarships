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
        st.write('How many scholarships are available?')
        st.write('How much are the scholarships worth?')
        st.write('What are the criteria of the scholarship?')
    if button('Edit Existing Scholarship', key='Edit Existing Scholarship'):
        st.write('form for editing')
    if button('Delete Existing Scholarship', key='Delete Existing Scholarship'):
        st.write('form for deleting')

#if button("Button 1", key="button1"):
#if button("Button 2", key="button2"):
#if button("Button 3", key="button3"):
