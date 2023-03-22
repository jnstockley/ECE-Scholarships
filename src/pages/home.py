'''
Home: Primary page for viewing student data, leaving reviews, and exporting selections
'''

# Packages used in code
import streamlit as st
import pandas as pd
from st_aggrid import JsCode, GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode

# Default setting for Streamlit page
st.set_page_config(layout="wide")

# Accessing test data (Will need to replace with Teams support)
df = pd.read_excel("./tests/data/ece_scholarship_applicants.xlsx", nrows=100)
df.insert(0, 'Selection', None)

scholarships = pd.read_excel("./tests/data/scholarships.xlsx")
user_recommendations = pd.read_excel("./tests/data/Test_User_Reviews.xlsx")
st.write(scholarships)

st.title("Home")
st.header("Review Applicants")

# Small function used to expand the paragrpah answers
clicked_name_cell_func = "function(params) { alert(params.node.data['Describe any relevant life experience related to engineering. ']); };"

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
gd.configure_column("Describe any relevant life experience related to engineering. ", headerTooltip='Click to see cell data', onCellClicked=JsCode(clicked_name_cell_func))
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
    allow_unsafe_jscode=True
)

# How to access selected rows for use in methods like reviewing
# sel_rows = grid_table["selected_rows"]

# Actions button that need to have functionality implemented
with st.container():
    col1, col2, col3= st.columns(3)
    with col1:
        with st.expander("Review Selected Students"):
            recommended_scholarship = st.selectbox("Select Scholarship to Recommend Students For:", scholarships.Name)
            additional_feedback = st.text_area("Enter any additional feedback on students")
            submit_recommendation = st.button("Submit Recommendation")
            if submit_recommendation:
                sel_uids = [key["UID"] for key in grid_table["selected_rows"]]
                new_recommendations = pd.DataFrame(columns= ['UID', 'Scholarship', 'Additional Feedback'])
                for uid in sel_uids:
                    new_recommendation = {"UID": uid, "Scholarship": recommended_scholarship, "Additional Feedback": additional_feedback}
                    new_recommendations = new_recommendations.append(new_recommendation, ignore_index=True)
                #new_recommendation = {"UID": , "Scholarship": , "Additional Feedback": }
                #Probably want to make a function that verifies the inputted students and whether or not they meet minimum criteria 
                st.write(new_recommendations)
                
                #Check for if they already recommended that student for that scholarship
                #Check if that scholarship has already been created
                #append_df_to_excel
                #Want it to refresh as well, clear the inputs, get rid of the collapse, and let them know it was a success
                #Also need to now who submitted it so we know where to save it to

    with col2:
        with st.expander("See Distribution of Selected Students"):
            st.write("Add Ashelyn's Data Analysis")
    with col3:
        st.button("Export Selected Students")
