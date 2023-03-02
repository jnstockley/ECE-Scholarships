'''
Home: Primary page for viewing student data, leaving reviews, and exporting selections
'''

# Packages used in code
import streamlit as st
import pandas as pd 
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode
from streamlit_extras.stateful_button import button

# Default setting for Streamlit page
st.set_page_config(layout="wide")

# Accessing test data (Will need to replace with Teams support)
df = pd.read_excel("./tests/data/ece_scholarship_applicants.xlsx", nrows=100)
df.insert(0, 'Selection', None)

st.title("Home")
st.header("Review Applicants")
current_filter = st.selectbox("Which filter would you like to apply?",
                              ("None", "Evan's custom filter", "Scholarship 1", "Scholarship 2"))
st.write("Current filter:", current_filter)

# Building the AgGrid Table
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True) #Add pagination
gd.configure_side_bar() #Add a sidebar
gd.configure_default_column(editable=False, groupable=True)
gd.configure_selection(selection_mode='multiple', use_checkbox=True) #Enable multi-row selection
gridoptions = gd.build()

custom_css = {}

grid_table = AgGrid(
    df, 
    gridOptions=gridoptions,
    theme='balham',
    custom_css=custom_css,
    height = 700,
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
)

sel_rows = grid_table["selected_rows"]
st.write(sel_rows)

with st.container():
    col1, col2, col3= st.columns(3)
    with col1:
        if button('Review Selected Students', key='Create New Scholarship'):
            st.write('form for creating')
    with col2:
        if button('See Distribution of Selected Students', key='Edit Existing Scholarship'):
            st.write('form for editing')
    with col3:
        if button('Export Selected Students', key='Delete Existing Scholarship'):
            st.write('form for deleting')