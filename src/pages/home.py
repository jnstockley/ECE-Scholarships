'''
Home: Primary page for viewing student data, leaving reviews, and exporting selections
'''

# Packages used in code
import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode
from streamlit_extras.stateful_button import button

from src.utils.html import redirect
from src.utils.sharepoint import logged_in

# Default setting for Streamlit page
st.set_page_config(layout="wide")

if not logged_in():
    redirect("/Log In")

# Accessing test data (Will need to replace with Teams support)
df = pd.read_excel("./tests/data/ece_scholarship_applicants.xlsx", nrows=100)
df.insert(0, 'Selection', None)

st.title("Home")
st.header("Review Applicants")

# Filter selection (Will want to implement this once we have example filters)
current_filter = st.selectbox("Which filter would you like to apply?",
                              ("None", "Evan's custom filter", "Scholarship 1", "Scholarship 2"))
st.write("Current filter:", current_filter)

# Configuring options for table functionality
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True) #Add pagination
gd.configure_side_bar() #Add a sidebar
gd.configure_default_column(editable=False, groupable=True)
gd.configure_selection(selection_mode='multiple', use_checkbox=True) #Enable multi-row selection
gridoptions = gd.build()

# Option to add custom css if want to change styling, right now using default theme
custom_css = {}

# Building the table
grid_table = AgGrid(
    df,
    gridOptions=gridoptions,
    theme='balham',
    custom_css=custom_css,
    height = 700,
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
)

# How to access selected rows for use in methods like reviewing
# sel_rows = grid_table["selected_rows"]

# Actions button that need to have functionality implemented
with st.container():
    col1, col2, col3= st.columns(3)
    with col1:
        if button('Review Selected Students', key='Create New Scholarship'):
            st.write("Will add form for leaving a review/feedback")
    with col2:
        if button('See Distribution of Selected Students', key='Edit Existing Scholarship'):
            st.write("Plug Ashelyn's Work in")
    with col3:
        if button('Export Selected Students', key='Delete Existing Scholarship'):
            st.write('Will present options for how to export')
