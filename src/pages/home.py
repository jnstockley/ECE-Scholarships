'''
Home: Primary page for viewing student data, leaving reviews, and exporting selections
'''

# Importing packages
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from st_aggrid import JsCode, GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode, GridUpdateMode

# Default settings for Streamlit page
st.set_page_config(layout="wide")

# Importing data
global STUDENTS
global SCHOLARSHIPS
global USER_RECOMMENDATIONS
STUDENTS = pd.read_excel("./tests/data/ece_scholarship_applicants.xlsx", nrows=100)
SCHOLARSHIPS = pd.read_excel("./tests/data/scholarships.xlsx")
USER_RECOMMENDATIONS = pd.read_excel("./tests/data/Test_User_Reviews.xlsx")

# Creating main dataframe
STUDENTS.insert(0, 'Select All', None)

# Helper functions for JavaScript
js = JsCode("""
 function(event) {
    const api = event.api; 
     window.addEventListener('clear.rows', (e) => {
         api.deselectAll(); 
     });    
 }
 """)
CLEARJS = '''<script>
     ((e) => {
        const iframe = window.parent.document.querySelectorAll('[title="st_aggrid.agGrid"]')[0] || null;
        if(!iframe) return;
        iframe.contentWindow.dispatchEvent( new Event('clear.rows'));
     })()
    </script>
    '''

# Start of display
st.title("Home")
st.header("Review Applicants")

# Filter selection (Will want to implement this once we have example filters)
current_filter = st.selectbox("Which scholarship criteria woudld you like to filter by?", np.append(["None"], SCHOLARSHIPS["Name"].values))

# Configuring options for table functionality
gd = GridOptionsBuilder.from_dataframe(STUDENTS)
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
    STUDENTS,
    gridOptions=gridoptions,
    theme='balham',
    custom_css=custom_css,
    height = 700,
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
    allow_unsafe_jscode=True,
    update_mode=GridUpdateMode.MODEL_CHANGED
)
st.write(len(grid_table["selected_rows"]))
# Displaying statistics about main data frame
st.write("Number of students selected: ", len([student["Name"] for student in grid_table["selected_rows"]]))
if st.button("Clear Selection"): 
    components.html(CLEARJS)

def submit_recommendations(recommended_scholarship, additional_feedback): 
    global USER_RECOMMENDATIONS
    if len(grid_table["selected_rows"]) == 0:
        return False, "Must select students to recommend"
    sel_uids = [key["UID"] for key in grid_table["selected_rows"]]
    new_recommendations = pd.DataFrame(columns= ['UID', 'Scholarship', 'Additional Feedback'])
    for uid in sel_uids:
        new_recommendation = {"UID": uid, "Scholarship": recommended_scholarship, "Additional Feedback": additional_feedback}
        if len(USER_RECOMMENDATIONS.loc[(USER_RECOMMENDATIONS['UID'] == uid) & (USER_RECOMMENDATIONS['Scholarship'] == recommended_scholarship)]) > 0: 
            return False, str("Already recommended student " + str(uid) + " for this scholarship")
        # Check here if students meets requirements of scholarship (Need to wait to merge Austin's PR before these)
        new_recommendations = new_recommendations.append(new_recommendation, ignore_index=True)
    # Check here for it too many recommendations for that scholarship, should be none if unlimited
    USER_RECOMMENDATIONS = USER_RECOMMENDATIONS.append(new_recommendations)
    USER_RECOMMENDATIONS.to_excel('./tests/data/Test_User_Reviews.xlsx', index = False)
    return True, None

# Actions for user to take on main data frame
with st.container():
    col1, col2, col3= st.columns(3)

    # Submitting recommendations for scholarhsips
    with col1:
        with st.expander("Review Selected Students"):
            with st.form("recommendation_form"):
                recommended_scholarship = st.selectbox("Select Scholarship to Recommend Students For:", SCHOLARSHIPS.Name)
                additional_feedback = st.text_area("Enter any additional feedback on students")
                submit_recommendation = st.form_submit_button("Submit Recommendation")            
                if "success" not in st.session_state:
                    st.session_state['success'] = False
                if "failure" not in st.session_state:
                    st.session_state['failure'] = False
                if "error" not in st.session_state:
                    st.session_state['error'] = False
                if st.session_state['success'] is True:
                    st.success("Successfuly submitted recommendations!")
                if st.session_state['failure'] is True:
                    st.error(st.session_state['error'])
                if submit_recommendation:
                    result, errorMessage = submit_recommendations(recommended_scholarship, additional_feedback)
                    if result is True:
                        st.session_state['success'] = True
                        st.session_state['failure'] = False
                    else:
                        st.session_state['success'] = False
                        st.session_state['failure'] = True
                        st.session_state['error'] = errorMessage
    # Viewing graphs of student distributions
    with col2:
        with st.expander("See Distribution of Selected Students"):
            st.write("Add Ashelyn's Data Analysis")
    # Exporting the selected students
    with col3:
        st.button("Export Selected Students")
