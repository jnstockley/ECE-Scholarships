'''
Home: Primary page for viewing student data, leaving reviews, and exporting selections
'''

# Packages used in code
import numbers
import decimal
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode
from streamlit_extras.stateful_button import button

# Default setting for Streamlit page
st.set_page_config(layout="wide")

# Accessing test data (Will need to replace with Teams support)
df = pd.read_excel("./tests/data/ece_scholarship_applicants.xlsx", nrows=100)
df.insert(0, 'Selection', None)

st.title("Home")
st.header("Review Applicants")

def dynamic_fig(df, x_axis, y_axis, highlights=None):
    '''
    Function to generate dynamic graph of student data
    '''
    fig, axis = plt.subplots()
    xs = df[x_axis][df[x_axis] != 0][df[y_axis] != 0]
    ys = df[y_axis][df[x_axis] != 0][df[y_axis] != 0]
    plt.scatter(xs, ys)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    #plt.legend(['<Highlighted Students>'])
    st.pyplot(fig)
    return fig, axis

with st.container():
    numeric_cols = df.copy().apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())
    numeric_cols = numeric_cols.loc[numeric_cols == True]
    numeric_cols = numeric_cols.drop(labels=['UID','Duplicate','Categorized At'],axis='index')
    numeric_cols = numeric_cols.append(pd.Series([True], index=['Upcoming Financial Need After Grants/Scholarships']))
    col1, _, _ = st.columns(3)
    with col1:
        fig_select1a = st.selectbox("Select X axis for graph 1",numeric_cols.index.values)
        fig_select1b = st.selectbox("Select Y axis for graph 1",numeric_cols.index.values)
        #sel_rows = grid_table["selected_rows"]
        #sel_row_indices = [rows['_selectedRowNodeInfo']['nodeRowIndex'] for rows in sel_rows]
        dynamic_fig(df, fig_select1a, fig_select1b)

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
