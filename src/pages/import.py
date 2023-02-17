
'''
Render view for import data page
'''
import streamlit as st
from src.utils.html import centered_text

st.title("Import Data")
st.write("Add files below, when finished press import to and the system will attempt to merge your files.")
st.file_uploader('')
st.markdown(centered_text('<em>supports both excel and csv format</em>'), unsafe_allow_html=True)
st.button('import')
