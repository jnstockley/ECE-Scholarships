'''
Home: Primary page for viewing student data, leaving reviews, and exporting selections
'''

# Importing packages
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from st_aggrid import JsCode, GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode, GridUpdateMode

# Default settings for Streamlit page
st.set_page_config(layout="wide")

# Importing data
students = pd.read_excel("./tests/data/ece_scholarship_applicants.xlsx", nrows=100)
scholarships = pd.read_excel("./tests/data/scholarships.xlsx")
user_recommendations = pd.read_excel("./tests/data/Test_User_Reviews.xlsx")

# Creating dataframe for home page
students.insert(0, 'Select All', None)


st.title("Home")
st.header("Review Applicants")

# Filter selection (Will want to implement this once we have example filters)
current_filter = st.selectbox("Which filter would you like to apply?",
                              ("None", "Scholarship 1", "Scholarship 2"))
st.write("Current filter:", current_filter)

js = JsCode("""
 function(event) {
    const api = event.api; 
     window.addEventListener('clear.rows', (e) => {
         api.deselectAll(); 
     });    
 }
 """)
clearJs = '''<script>
     ((e) => {
        const iframe = window.parent.document.querySelectorAll('[title="st_aggrid.agGrid"]')[0] || null;
        if(!iframe) return;
        iframe.contentWindow.dispatchEvent( new Event('clear.rows'));
     })()
    </script>
    '''
# Configuring options for table functionality
gd = GridOptionsBuilder.from_dataframe(students)
gd.configure_pagination(enabled=True) #Add pagination
gd.configure_side_bar() #Add a sidebar
gd.configure_default_column(editable=False, groupable=True)
gd.configure_selection(selection_mode='multiple', use_checkbox=True) #Enable multi-row selection
gd.configure_column("Select All", headerCheckboxSelection = True)
gd.configure_grid_options(onFirstDataRendered=js)
gd.configure_column("Describe any relevant life experience related to engineering. ", onCellClicked=JsCode("function(params) { alert(params.node.data['Describe any relevant life experience related to engineering. ']); };"))
gridoptions = gd.build()

# Option to add custom css if want to change styling, right now using default theme
custom_css = {}

# Building the table
grid_table = AgGrid(
    students,
    gridOptions=gridoptions,
    theme='balham',
    custom_css=custom_css,
    height = 700,
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
    allow_unsafe_jscode=True,
    update_mode=GridUpdateMode.MODEL_CHANGED
)
st.write("Number of students selected: ", len([student["Name"] for student in grid_table["selected_rows"]]))

with st.container():
    col1, col2, col3= st.columns(3)
    with col1:
        with st.expander("Review Selected Students", expanded = False):
            with st.form("recommendation_form", clear_on_submit=True):
                recommended_scholarship = st.selectbox("Select Scholarship to Recommend Students For:", scholarships.Name)
                additional_feedback = st.text_area("Enter any additional feedback on students")
                submit_recommendation = st.form_submit_button("Submit Recommendation")
                if submit_recommendation:
                    sel_uids = [key["UID"] for key in grid_table["selected_rows"]]
                    new_recommendations = pd.DataFrame(columns= ['UID', 'Scholarship', 'Additional Feedback'])
                    for uid in sel_uids:
                        new_recommendation = {"UID": uid, "Scholarship": recommended_scholarship, "Additional Feedback": additional_feedback}
                        new_recommendations = new_recommendations.append(new_recommendation, ignore_index=True)
                    user_recommendations = user_recommendations.append(new_recommendations)
                    user_recommendations.to_excel('./tests/data/Test_User_Reviews.xlsx', index = False)
                    components.html(clearJs)



    with col2:
        with st.expander("See Distribution of Selected Students"):
            st.write("Add Ashelyn's Data Analysis")
    with col3:
        st.button("Export Selected Students")
