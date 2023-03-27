'''
Export data page
'''
import streamlit as st
from src.sessions.session_manager import SessionManager

SESSION = SessionManager(st.session_state, "single")

st.header('Export Data')
# check if there is data in session
# if no data show error, you need to import data first!
# if is data, show export button which will open a save menu
