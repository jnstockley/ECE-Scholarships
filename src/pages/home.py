'''
Home: Primary page for viewing student data, leaving reviews, and exporting selections
'''

# Importing packages
# Packages used in code
import os
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from st_aggrid import JsCode, GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode, GridUpdateMode
import matplotlib.pyplot as plt
from matplotlib import cm

from src.utils.html import redirect
from src.utils.sharepoint import logged_in, download, upload, login
from src.utils.scholarship_management import edit_row

# Default setting for Streamlit page
st.set_page_config(layout="wide")

# Log in protecting the home page
cookie = logged_in()

if not cookie:
   redirect("/Log In")

@st.cache_data
def download_data():

    with st.spinner("Loading Data from Sharepoint..."):
        
        creds = login(cookie)

        hawk_id = cookie.get('cred')['hawk-id']

        download('/data/Master_Sheet.xlsx', f"{os.getcwd()}/data/", creds)
        download('/data/Scholarships.xlsx', f"{os.getcwd()}/data/", creds)
        try:
            download(f'/data/{hawk_id}_Reviews.xlsx', f"{os.getcwd()}/data/", creds)
        except:
            new_file = pd.DataFrame(columns= ['UID', 'Scholarship', 'Rating', 'Additional Feedback'])
            new_file.to_excel(f'./data/{hawk_id}_Reviews.xlsx', index = False)
            upload(os.path.abspath(f'./data/{hawk_id}_Reviews.xlsx'), '/data/', creds)
 
        return creds, hawk_id
    
creds, hawk_id = download_data()

# Importing data
if 'students' not in st.session_state:
    st.session_state.students = pd.read_excel("./data/Master_Sheet.xlsx")
    students = st.session_state.students
    # Creating main dataframe
    students.insert(0, 'Select All', None)
else: 
    students = st.session_state.students

if 'scholarships' not in st.session_state:
    st.session_state.scholarships = pd.read_excel("./data/Scholarships.xlsx")
    scholarships = st.session_state.scholarships
else: 
    scholarships = st.session_state.scholarships

if 'user_recommendations' not in st.session_state: 
    st.session_state.user_recommendations = pd.read_excel(f"./data/{hawk_id}_Reviews.xlsx")
    user_recommendations = st.session_state.user_recommendations
else: 
    user_recommendations = st.session_state.user_recommendations



st.write(user_recommendations)

# Helper functions for JavaScript
js = JsCode("""
 function(event) {
    const api = event.api; 
     window.addEventListener('clear.rows', (e) => {
         api.deselectAll(); 
     });    
 }
 """)
jscode = JsCode("""
            function(params) {
                if (params.data.review === 'yes') {
                    return {
                        'color': 'white',
                        'backgroundColor': 'green'
                    }
                }
                if (params.data.review === 'no') {
                    return {
                        'color': 'white',
                        'backgroundColor': 'red'
                    }
                }
                if (params.data.review === 'maybe') {
                    return {
                        'color': 'white',
                        'backgroundColor': 'yellow'
                    }
                }
            };
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

def dynamic_fig(var_df, x_axis, y_axis, highlights=None):
    '''
    Function to generate dynamic graph of student data
    '''
    fig, axis = plt.subplots()
    var_xs = var_df[x_axis][var_df[x_axis] != 0][var_df[y_axis] != 0]
    var_ys = var_df[y_axis][var_df[x_axis] != 0][var_df[y_axis] != 0]
    plt.scatter(var_xs, var_ys)
    if highlights is not None:
        hxs = var_df.iloc[highlights][x_axis]
        hys = var_df.iloc[highlights][y_axis]
        colors = iter(cm.rainbow(np.linspace(0, 1, len(hys)+1)))
        next(colors)
        for var_x, var_y in zip(hxs,hys):
            plt.scatter(var_x, var_y, color=next(colors))
        legend_names = ['Other Students']
        legend_names.extend(var_df.iloc[highlights]['Name'].values)
        plt.legend(legend_names)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    st.pyplot(fig)
    return fig, axis



# Filter selection (Will want to implement this once we have example filters)
current_scholarship = st.selectbox("Which scholarship would you like to consider?", np.append(["None"], scholarships["Name"].values))

# Configuring options for table functionality
gd = GridOptionsBuilder.from_dataframe(students)
gd.configure_pagination(enabled=True) #Add pagination
gd.configure_side_bar() #Add a sidebar
gd.configure_default_column(editable=False, groupable=True)
gd.configure_selection(selection_mode='multiple', use_checkbox=True) #Enable multi-row selection
gd.configure_column("Select All", headerCheckboxSelection = True)
gd.configure_grid_options(onFirstDataRendered=js)
gd.configure_column("Describe any relevant life experience related to engineering. ",
                    onCellClicked=JsCode("function(params) { alert(params.node.data['Describe any relevant life experience related to engineering. ']); };"))
gridoptions = gd.build()
gridoptions['getRowStyle'] = jscode

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

# Displaying statistics about main data frame
st.write("Number of students selected: ", len([student["Name"] for student in grid_table["selected_rows"]]))
if st.button("Clear Selection"):
    components.html(CLEARJS)


# How to access selected rows for use in methods like reviewing
# sel_rows = grid_table["selected_rows"]

# Helper function used for processing the scholarship recommendations
def submit_recommendations(user_recommendations, recommended_scholarship, rating, additional_feedback):
    if len(grid_table["selected_rows"]) == 0:
        return False, "Must select students to recommend"
    sel_uids = [key["UID"] for key in grid_table["selected_rows"]]
    new_recommendations = pd.DataFrame(columns= ['UID', 'Scholarship', 'Rating', 'Additional Feedback'])
    for uid in sel_uids:
        new_recommendation = {"UID": uid, "Scholarship": recommended_scholarship, "Rating": rating, "Additional Feedback": additional_feedback}
        if len(user_recommendations.loc[(user_recommendations['UID'] == uid) & (user_recommendations['Scholarship'] == recommended_scholarship)]) > 0:
            return False, str("Already reviewed student " + str(uid) + " for this scholarship")
        # Check here if students meets requirements of scholarship (Need to wait to merge Austin's PR before these)
        new_recommendations = new_recommendations.append(new_recommendation, ignore_index=True)
    # Check here for it too many recommendations for that scholarship, should be none if unlimited
    user_recommendations = user_recommendations.append(new_recommendations)
    user_recommendations.to_excel(f'./data/{hawk_id}_Reviews.xlsx', index = False)
    upload(os.path.abspath(f'./data/{hawk_id}_Reviews.xlsx'), '/data/', creds)
    return True, user_recommendations


# Actions for user to take on main data frame
with st.container():
    col1, col2, col3= st.columns(3)

    # Submitting recommendations for scholarhsips
    with col1:
        with st.expander("Review Selected Students"):
            if current_scholarship == "None":
                st.error('Must Select a Scholarship to Review For')
            else: 
                with st.form("recommendation_form"):
                    st.write(f'Review for Scholarship: {current_scholarship}')
                    rating = st.selectbox("Would you recommend these students for this scholarship?", ['Yes', 'No', 'Maybe'])
                    additional_feedback = st.text_area("Enter any additional feedback on students")
                    submit_recommendation = st.form_submit_button("Submit Recommendation")
                    if 'review_success' in st.session_state:
                        if st.session_state.review_success == 'success':
                            st.success("Successfuly submitted recommendations!")
                        if st.session_state.review_success == 'error':
                            st.error(st.session_state.review_result)
                    if submit_recommendation:
                        success, result = submit_recommendations(user_recommendations, current_scholarship, rating, additional_feedback)
                        if success is True:
                            st.session_state.user_recommendations = result
                            st.session_state.review_success = 'success'
                            st.experimental_rerun()
                        else:
                            st.session_state.review_success = 'error'
                            st.session_state.review_result = result
                            st.experimental_rerun()

    # Viewing graphs of student distributions
    with col2:
        with st.expander("See Distribution of Students"):
            with st.container():
                numeric_cols = students.copy().apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())
                numeric_cols = numeric_cols.loc[numeric_cols == True]
                numeric_cols = numeric_cols.drop(labels=['UID','Duplicate','Categorized At'],axis='index')
                numeric_cols = numeric_cols.append(pd.Series([True], index=['Upcoming Financial Need After Grants/Scholarships']))
                fig_select1a = st.selectbox("Select X axis for graph 1",numeric_cols.index.values)
                fig_select1b = st.selectbox("Select Y axis for graph 1",numeric_cols.index.values)
                sel_rows = grid_table["selected_rows"]
                sel_row_indices = [rows['_selectedRowNodeInfo']['nodeRowIndex'] for rows in sel_rows]
                dynamic_fig(students, fig_select1a, fig_select1b, sel_row_indices)    # Exporting the selected students
    with col3:
        st.button("Export Selected Students")
