'''
Homepage view.
'''
import streamlit as st
import pandas as pd 
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

st.set_page_config(layout="wide")

data = pd.read_excel("./tests/data/ece_scholarship_applicants.xlsx", nrows=15)

AgGrid(data)

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
    height=350, 
    width='100%',
    reload_data=True
)

data = grid_response['data']
selected = grid_response['selected_rows'] 
df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df

st.title('Review Applicants')

current_filter = st.selectbox("Which filter would you like to apply?",
                              ("Evan's custom filter", "Scholarship 1", "Scholarship 2"))

st.write("Current filter:", current_filter)

st.write("***Example With Actions")
colms = st.columns((1, 2, 1, 1, 1))
fields = ["UID", "Name", "Program", "Sex", "Review"]
for col, field_name in zip(colms, fields):
    col.write(field_name)

for x, uid in enumerate(data["UID"]):
    col1, col2, col3, col4, col5 = st.columns((1, 2, 1, 1, 1))
    col1.write(uid)
    col2.write(data["Name"][x])
    col3.write(data["Programs"][x])
    col4.write(data["Sex"][x])
    REVIEWED = False
    BUTTON_TYPE = "Review" if not REVIEWED else "Rereview"
    button_phold = col5.empty()  # create a placeholder
    do_action = button_phold.button(BUTTON_TYPE, key=x)
    if do_action:
        # do some action with a row's data
        button_phold.empty()  # remove button


st.write("***Example with Built In Table")
st.dataframe(data)

st.button("Export current data")
