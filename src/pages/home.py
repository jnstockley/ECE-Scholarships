'''
Home: Primary page for viewing student data, leaving reviews, and exporting selections
'''

# Packages used in code
import streamlit as st
import pandas as pd 
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

# Default setting for Streamlit page
st.set_page_config(layout="wide")

# Accessing test data (Will need to replace with Teams support)
data = pd.read_excel("./tests/data/ece_scholarship_applicants.xlsx", nrows=15)

st.title("Home")
st.header("Review Applicants")
current_filter = st.selectbox("Which filter would you like to apply?",
                              ("Evan's custom filter", "Scholarship 1", "Scholarship 2"))
st.write("Current filter:", current_filter)
gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
gb.configure_side_bar() #Add a sidebar
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection

gridOptions = gb.build()

grid_response = AgGrid(
    data,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    theme='material', #Add theme color to the table
    enable_enterprise_modules=True,
    height=700, 
    width='100%',
    reload_data=True
)

data = grid_response['data']
selected = grid_response['selected_rows']
df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

st.button("Export current data")
