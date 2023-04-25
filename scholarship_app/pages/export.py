'''
Export data page
'''
import streamlit as st
from sessions.session_manager import SessionManager
from utils.output import get_output_dir

SESSION = SessionManager(st.session_state, "single")

st.header('Export Data')
if not hasattr(SESSION, "data"):
    st.write("Once you've imported data you can return to this page to export it the combined excel sheet")
else:
    st.write("Download your merged data locally")

    SESSION.data.to_excel(f"{get_output_dir()}/student_data_export.xls")

    with open(f"{get_output_dir()}/student_data_export.xls", "rb") as file:
        st.download_button(
                label="Export",
                data=file,
                file_name="student_data_export.xls",
                mime="image/png"
            )
