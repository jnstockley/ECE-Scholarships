import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from st_aggrid import AgGrid

CLEARJS = """<script>
     ((e) => {
        const iframe = window.parent.document.querySelectorAll('[title="st_aggrid.agGrid"]')[0] || null;
        if(!iframe) return;
        iframe.contentWindow.dispatchEvent( new Event('clear.rows'));
     })()
    </script>
    """


def main_data_statistics(
    current_data: pd.DataFrame, students: pd.DataFrame, grid_table: AgGrid
):
    """
    Renders the table statistics found below the main homepage table.
    """
    with st.container():
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(
                "Key: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **<span style='color:#00B985'>Yes</span>**"
                + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **<span style='color:#EA0101'>No</span>**"
                + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **<span style='color:#D6D600'>Maybe</span>**",
                unsafe_allow_html=True,
            )
        with col2:
            st.write(
                "Number of Students: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Selected: ",
                len([student["Name"] for student in grid_table["selected_rows"]]),
                unsafe_allow_html=True,
            )
        with col3:
            st.write("Eligible for Selected Scholarship: ", len(current_data))
        with col4:
            st.write(
                "Ineligible for Selected Scholarship: ",
                len(students) - len(current_data),
            )
        with col5:
            if st.button("Clear Selection"):
                components.html(CLEARJS)
