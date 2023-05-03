'''
Home: Primary page for viewing student data, leaving reviews, and exporting selections
'''

# Importing packages
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from st_aggrid import JsCode, GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode, GridUpdateMode
from matplotlib import cm
from src.utils.html import redirect
from src.managers.sharepoint.sharepoint_session import SharepointSession
from src.utils.scholarship_management import groups_string_to_list
from src.utils.output import get_appdata_path

# Default setting for Streamlit page
st.set_page_config(layout="wide")

SHAREPOINT = SharepointSession(st.session_state)
if not SHAREPOINT.is_signed_in():
    redirect("/Account")

# Setting variables for script
if 'students' not in st.session_state:
    SHAREPOINT.download('/data/Master_Sheet.xlsx', "/data/")
    st.session_state.students = pd.read_excel(get_appdata_path("/data/Master_Sheet.xlsx"))
students = st.session_state_students
current_data = students.copy()
if 'scholarships' not in st.session_state:
    SHAREPOINT.download('/data/Scholarships.xlsx', "/data/")
    st.session_state.scholarships = pd.read_excel(get_appdata_path("/data/Scholarships.xlsx"))
scholarships = st.session_state_scholarships
if 'user_recommendations' not in st.session_state:
    try:
        SHAREPOINT.download(f'/data/{SHAREPOINT.get_hawk_id()}_Reviews.xlsx', "/data/")
    except:
        new_file = pd.DataFrame(columns= ['UID', 'Scholarship', 'Rating', 'Additional Feedback'])
        new_file.to_excel(get_appdata_path(f'/data/{SHAREPOINT.get_hawk_id()}_Reviews.xlsx'), index = False)
        SHAREPOINT.upload(f"/data/{SHAREPOINT.get_hawk_id()}_Reviews.xlsx", '/data/')
    st.session_state.user_recommendations = pd.read_excel(get_appdata_path(f"/data/{SHAREPOINT.get_hawk_id()}_Reviews.xlsx"))
user_recommendations = st.session_state.user_recommendations


# JavaScript functions for styling table
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
                if (params.data.Review === 'Yes') {
                    return {
                        'color': 'white',
                        'backgroundColor': '#017252'
                    }
                }
                if (params.data.Review === 'No') {
                    return {
                        'color': 'white',
                        'backgroundColor': '#8E0303'
                    }
                }
                if (params.data.Review === 'Maybe') {
                    return {
                        'color': 'white',
                        'backgroundColor': '#A2A200'
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

# Start of displayed page
st.title("Home")
st.header("Review Applicants")

# Selecting a scholarship to use for filtering and reviews
current_scholarship = st.selectbox("Which scholarship would you like to consider?", np.append(["None"], scholarships["Name"].values))
if current_scholarship != "None":

    # Adding previos reviews to current data
    current_data_reviews = []
    for index, row in current_data.iterrows():
        student_recommendation = user_recommendations.loc[(user_recommendations['UID'] == row['UID']) & (user_recommendations['Scholarship'] == current_scholarship)]
        if len(student_recommendation) > 0:
            current_data_reviews.append(student_recommendation['Rating'].iloc[0])
        else:
            current_data_reviews.append('N/A')
    current_data['Review'] = current_data_reviews

    # Filtering current data with scholarship criteria
    criteria = scholarships.loc[scholarships['Name'] == current_scholarship]
    criteria_index = scholarships
    groups_columns = []
    criteria_no_groups = []
    for column in criteria.columns.tolist():
        if column[0:5] == "Group":
            if isinstance(criteria[column].iloc[0], str) and criteria[column].iloc[0].startswith('[') and criteria[column].iloc[0].endswith(']'):
                groups_columns.append(groups_string_to_list(criteria[column].iloc[0]))
        elif column not in ['Name', 'Total Amount', 'Value']:
            criteria_no_groups.append(column)
    for criterion in criteria_no_groups:
        if criterion in current_data.columns.tolist():
            try:
                value = float(criteria[criterion])
                IN_GROUP = False
                for group in groups_columns:
                    if criterion in group:
                        IN_GROUP = True
                        MET_CRITERIA = False
                        for index, student in current_data.iterrows():
                            for group_c in group:
                                if student[group_c] >= value:
                                    MET_CRITERIA = True
                            if MET_CRITERIA == False:
                                current_data.drop(index)
                if IN_GROUP == False:
                    current_data.drop(current_data.loc[current_data[criterion] < value].index, inplace = True)
            except ValueError:
                value = criteria[criterion]
                IN_GROUP = False
                for group in groups_columns:
                    if criterion in group:
                        IN_GROUP = True
                        MET_CRITERIA = False
                        for index, student in current_data.iterrows():
                            for group_c in group:
                                if student[group_c] >= value:
                                    MET_CRITERIA = True
                            if MET_CRITERIA == False:
                                current_data.drop(index)
                if IN_GROUP == False:
                    current_data.drop(current_data.loc[current_data[criterion] != value].index, inplace = True)

# Configuring options for table functionality
current_data.insert(0, 'Select All', None)
gd = GridOptionsBuilder.from_dataframe(current_data)
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
custom_css = {}

# Building the table
grid_table = AgGrid(
    current_data,
    gridOptions=gridoptions,
    theme='balham',
    custom_css=custom_css,
    height = 700,
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
    allow_unsafe_jscode=True,
    update_mode=GridUpdateMode.MODEL_CHANGED
)

# Displaying statistics about main data frame
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("Key: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **<span style='color:#00B985'>Yes</span>**"
                    + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **<span style='color:#EA0101'>No</span>**"
                    + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **<span style='color:#D6D600'>Maybe</span>**", unsafe_allow_html=True)
    with col2:
        st.write("Number of Students: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Selected: ", len([student["Name"] for student in grid_table["selected_rows"]]), unsafe_allow_html=True)
    with col3:
        st.write("Eligible for Selected Scholarship: ", len(current_data))
    with col4:
        st.write("Ineligible for Selected Scholarship: ", len(students) - len(current_data))
    with col5:
        if st.button("Clear Selection"):
            components.html(CLEARJS)

# Helper function used for processing the scholarship reviews
def submit_recommendations(user_recommendations_input, recommended_scholarship, rating_input, additional_feedback_input):
    '''
    Method used to complete the review process by updating local and sharepoint data
    '''
    if len(grid_table["selected_rows"]) == 0:
        return False, "Must select students to recommend"
    sel_uids = [key["UID"] for key in grid_table["selected_rows"]]
    new_recommendations = pd.DataFrame(columns= ['UID', 'Scholarship', 'Rating', 'Additional Feedback'])
    for uid in sel_uids:
        new_recommendation = {"UID": uid, "Scholarship": recommended_scholarship, "Rating": rating_input, "Additional Feedback": additional_feedback_input}
        if len(user_recommendations_input.loc[(user_recommendations_input['UID'] == uid) & (user_recommendations_input['Scholarship'] == recommended_scholarship)]) > 0:
            return False, str("Already reviewed student " + str(uid) + " for this scholarship")
        # Check here if students meets requirements of scholarship (Need to wait to merge Austin's PR before these)
        new_recommendations = new_recommendations.append(new_recommendation, ignore_index=True)
    # Check here for it too many recommendations for that scholarship, should be none if unlimited
    user_recommendations_input = user_recommendations_input.append(new_recommendations)
    user_recommendations_input.to_excel(get_appdata_path(f"/data/{SHAREPOINT.get_hawk_id()}_Reviews.xlsx"), index = False)

    SHAREPOINT.upload(f"/data/{SHAREPOINT.get_hawk_id()}_Reviews.xlsx", '/data/')

    return True, user_recommendations_input

# Helper function for graph
def dynamic_fig(var_df, x_axis, y_axis, options=None, highlights=None):
    '''
    Function to generate dynamic graph of student data
    '''
    fig, _ = plt.subplots()
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
    for wbin in weighted_bins:
        if options[1]:
            wbin[-1] = wbin[-1] - (np.min(weighted_bins[:,2])-1)
        else:
            wbin[-1] = 1
        if wbin[-1] > 10:
            wbin[-1] = 10
    plt.scatter(weighted_bins[:,0], weighted_bins[:,1], s=32*weighted_bins[:,2])
    if highlights is not None and options[2] == 'Selected Students':
        highlights = [h for h in highlights if h is not None]
        hxs = var_df.iloc[highlights][x_axis]
        hys = var_df.iloc[highlights][y_axis]
        colors = iter(cm.rainbow(np.linspace(0, 1, len(hys)+1)))
        next(colors)
        for var_x, var_y in zip(hxs,hys):
            plt.scatter(var_x, var_y, color=next(colors))
        legend_names = ['Other Students']
        legend_names.extend(var_df.iloc[highlights]['Name'].values)
        if options[0]:
            plt.legend(legend_names)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    st.pyplot(fig)
    return fig

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
                            st.session_state['review_success'] = None
                        if st.session_state.review_success == 'error':
                            st.error(st.session_state.review_result)
                            st.session_state['review_success'] = None
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
                numeric_cols = current_data.copy().apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())
                numeric_cols = numeric_cols.loc[numeric_cols == True]
                for label in ['UID','Duplicate','Categorized At']:
                    try:
                        numeric_cols = numeric_cols.drop(labels=[label],axis='index')
                    except:
                        print('column not found:',label)
                #numeric_cols = numeric_cols.drop(labels=['UID','Duplicate','Categorized At'],axis='index')
                numeric_cols = numeric_cols.append(pd.Series([True], index=['Upcoming Financial Need After Grants/Scholarships']))
                fig_select1a = st.selectbox("Select X axis",numeric_cols.index.values)
                fig_select1b = st.selectbox("Select Y axis",numeric_cols.index.values)
                fig_select1c = st.selectbox("Highlight Scheme", ['None', 'Selected Students'])#, 'Scholarship Status'
                show_legend = st.checkbox("Show Legend", True)
                weight_bins = st.checkbox("Weight Plot", True)
                SEL_ROW_INDICES = None
                if fig_select1c == 'Selected Students':
                    sel_rows = grid_table["selected_rows"]
                    SEL_ROW_INDICES = [rows['_selectedRowNodeInfo']['nodeRowIndex'] for rows in sel_rows]
                option_select = [show_legend, weight_bins, fig_select1c]
                dynamic_fig(current_data, fig_select1a, fig_select1b, option_select, SEL_ROW_INDICES)    # Exporting the selected students
    with col3:
        if st.button("Export Current Table"):
            grid_table['data'].to_excel(get_appdata_path('./data/Exported_Data.xlsx'))
            st.success('Exported data to /data as Exported_Data.xlsx')
