'''
Home: Primary page for viewing student data, leaving reviews, and exporting selections
'''

# Importing packages
# Packages used in code
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
from st_aggrid import JsCode, GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode, GridUpdateMode
import matplotlib.pyplot as plt
from matplotlib import cm

from src.utils.html import redirect
from src.utils.sharepoint import logged_in

# Default setting for Streamlit page
st.set_page_config(layout="wide")

if not logged_in():
    redirect("/Log In")

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

def dynamic_fig(var_df, x_axis, y_axis, show_legend = False, highlight_select = 'None', highlights=None):
    '''
    Function to generate dynamic graph of student data
    '''
    fig, axis = plt.subplots()
    var_xs = var_df[x_axis][var_df[x_axis] != 0][var_df[y_axis] != 0]
    var_ys = var_df[y_axis][var_df[x_axis] != 0][var_df[y_axis] != 0]
    weighted_bins = np.zeros((len(var_xs),3))
    for i in var_xs.index:
        found = False
        for j in range(weighted_bins.shape[0]):
            if found:
                continue
            if weighted_bins[j][0] == 0 or (weighted_bins[j][0] == var_xs[i] and weighted_bins[j][1] == var_ys[i]):
                weighted_bins[j][0] = var_xs[i]
                weighted_bins[j][1] = var_ys[i]
                weighted_bins[j][2] += 1
                found = True
    weighted_bins = weighted_bins[~np.all(weighted_bins == 0, axis=1)]
    plt.scatter(weighted_bins[:,0], weighted_bins[:,1], s=32*weighted_bins[:,2])
    if highlights is not None and highlight_select == 'Selected Students':
        hxs = var_df.iloc[highlights][x_axis]
        hys = var_df.iloc[highlights][y_axis]
        colors = iter(cm.rainbow(np.linspace(0, 1, len(hys)+1)))
        next(colors)
        for var_x, var_y in zip(hxs,hys):
            plt.scatter(var_x, var_y, color=next(colors))
        legend_names = ['Other Students']
        legend_names.extend(var_df.iloc[highlights]['Name'].values)
        if show_legend:
            plt.legend(legend_names)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    st.pyplot(fig)
    return fig, axis



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
gd.configure_column("Describe any relevant life experience related to engineering. ",
                    onCellClicked=JsCode("function(params) { alert(params.node.data['Describe any relevant life experience related to engineering. ']); };"))
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

# Displaying statistics about main data frame
st.write("Number of students selected: ", len([student["Name"] for student in grid_table["selected_rows"]]))
if st.button("Clear Selection"):
    components.html(CLEARJS)


# How to access selected rows for use in methods like reviewing
# sel_rows = grid_table["selected_rows"]

# Helper function used for processing the scholarship recommendations
def submit_recommendations(recommended_scholarship_input, additional_feedback_input):
    """Solving pylint error"""
    global USER_RECOMMENDATIONS
    if len(grid_table["selected_rows"]) == 0:
        return False, "Must select students to recommend"
    sel_uids = [key["UID"] for key in grid_table["selected_rows"]]
    new_recommendations = pd.DataFrame(columns= ['UID', 'Scholarship', 'Additional Feedback'])
    for uid in sel_uids:
        new_recommendation = {"UID": uid, "Scholarship": recommended_scholarship_input, "Additional Feedback": additional_feedback_input}
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
                if submit_recommendation:
                    result, errorMessage = submit_recommendations(recommended_scholarship, additional_feedback)
                    if result is True:
                        st.success("Successfuly submitted recommendations!")
                    else:
                        st.error(errorMessage)
    # Viewing graphs of student distributions
    with col2:
        with st.expander("See Distribution of Students"):
            with st.container():
                numeric_cols = STUDENTS.copy().apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())
                numeric_cols = numeric_cols.loc[numeric_cols == True]
                numeric_cols = numeric_cols.drop(labels=['UID','Duplicate','Categorized At'],axis='index')
                numeric_cols = numeric_cols.append(pd.Series([True], index=['Upcoming Financial Need After Grants/Scholarships']))
                fig_select1a = st.selectbox("Select X axis",numeric_cols.index.values)
                fig_select1b = st.selectbox("Select Y axis",numeric_cols.index.values)
                fig_select1c = st.selectbox("Highlight Scheme", ['None', 'Selected Students', 'Scholarship Status'])
                show_legend = st.checkbox("Show Legend", True)
                sel_rows = grid_table["selected_rows"]
                sel_row_indices = [rows['_selectedRowNodeInfo']['nodeRowIndex'] for rows in sel_rows]
                dynamic_fig(STUDENTS, fig_select1a, fig_select1b, show_legend, fig_select1c, sel_row_indices)    # Exporting the selected students
    with col3:
        st.button("Export Selected Students")
