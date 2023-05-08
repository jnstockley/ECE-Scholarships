"""
Export data page
"""
import streamlit as st
from scholarship_app.managers.sharepoint.sharepoint_session import SharepointSession
from scholarship_app.utils.output import get_appdata_path
from scholarship_app.managers.sharepoint.file_versioning import DataManager, DataType
from scholarship_app.utils.html import redirect

SHAREPOINT = SharepointSession(st.session_state)
if not SHAREPOINT.is_signed_in():
    redirect("/Account")

MAIN_DATA = DataManager(st.session_state, DataType.MAIN, SHAREPOINT)

st.header("Export Data")
with st.spinner("Downloading Data..."):
    main_data = MAIN_DATA.retrieve_master()

if main_data is None:
    st.write(
        "No master data imported, once you import data and save it to the master sheet in sharepoint you can return to export data and download that sheet at any point"
    )
else:
    st.write("Download your sharepoint master datasheet")

    main_data.to_excel(f"{get_appdata_path('temp/download')}/student_data_export.xls")

    with open(
        f"{get_appdata_path('temp/download')}/student_data_export.xls", "rb"
    ) as file:
        st.download_button(
            label="Export",
            data=file,
            file_name="student_data_export.xls",
            mime="image/png",
        )
