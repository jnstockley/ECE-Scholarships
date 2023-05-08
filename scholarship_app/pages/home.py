"""
Home: Primary page for viewing student data, leaving reviews, and exporting selections
"""
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import (
    JsCode,
    GridOptionsBuilder,
    AgGrid,
    ColumnsAutoSizeMode,
    GridUpdateMode,
)

from scholarship_app.utils.html import redirect
from scholarship_app.managers.sharepoint.sharepoint_session import SharepointSession
from scholarship_app.utils.scholarship_management import groups_string_to_list
from scholarship_app.utils.output import get_appdata_path
from scholarship_app.managers.sharepoint.file_versioning import DataManager, DataType
from scholarship_app.sessions.session_manager import SessionManager
from scholarship_app.components.home.graphing import dynamic_fig
from scholarship_app.components.home.statistics import main_data_statistics

# Default setting for Streamlit page
st.set_page_config(layout="wide")

SHAREPOINT = SharepointSession(st.session_state)
if not SHAREPOINT.is_signed_in():
    redirect("/Account")

MAIN_DATA = DataManager(st.session_state, DataType.MAIN, SHAREPOINT)
SESSION = SessionManager(st.session_state, "home", "download")

js = JsCode(
    """
 function(event) {
    const api = event.api; 
     window.addEventListener('clear.rows', (e) => {
         api.deselectAll(); 
     });    
 }
 """
)
jscode = JsCode(
    """
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
            """
)

# Start of displayed page
st.title("Home")
st.header("Review Applicants")


def error_view():
    """
    Displays no data error
    """
    if MAIN_DATA.retrieve_master() is not None:
        SESSION.set_view("download")
    st.error(
        "Unable to reference master sheet in sharepoint. You must import data first"
    )


def downloading_data_view():
    """
    The downloading data view which also initializes the homepage session with necessary data.
    """
    with st.spinner("Downloading Data..."):
        master_sheet = MAIN_DATA.retrieve_master()

        if "students" not in st.session_state and not master_sheet is None:
            st.session_state.students = master_sheet

        if "scholarships" not in st.session_state:
            SHAREPOINT.download("/data/Scholarships.xlsx", "/data/")
            st.session_state.scholarships = pd.read_excel(
                get_appdata_path("/data/Scholarships.xlsx")
            )

        if "user_recommendations" not in st.session_state:
            try:
                SHAREPOINT.download(
                    f"/data/{SHAREPOINT.get_hawk_id()}_Reviews.xlsx", "/data/"
                )
            except:
                new_file = pd.DataFrame(
                    columns=["UID", "Scholarship", "Rating", "Additional Feedback"]
                )
                new_file.to_excel(
                    get_appdata_path(f"/data/{SHAREPOINT.get_hawk_id()}_Reviews.xlsx"),
                    index=False,
                )
                SHAREPOINT.upload(
                    f"/data/{SHAREPOINT.get_hawk_id()}_Reviews.xlsx", "/data/"
                )
            st.session_state.user_recommendations = pd.read_excel(
                get_appdata_path(f"/data/{SHAREPOINT.get_hawk_id()}_Reviews.xlsx")
            )

    SESSION.set_view("main")


def submit_recommendations(
    user_recommendations_input,
    recommended_scholarship,
    rating_input,
    additional_feedback_input,
    grid_table,
):
    """
    Helper function used for processing the scholarship reviews
    Method used to complete the review process by updating local and sharepoint data
    """
    if len(grid_table["selected_rows"]) == 0:
        return False, "Must select students to recommend"
    sel_uids = [key["UID"] for key in grid_table["selected_rows"]]
    new_recommendations = pd.DataFrame(
        columns=["UID", "Scholarship", "Rating", "Additional Feedback"]
    )
    for uid in sel_uids:
        new_recommendation = {
            "UID": uid,
            "Scholarship": recommended_scholarship,
            "Rating": rating_input,
            "Additional Feedback": additional_feedback_input,
        }
        if (
            len(
                user_recommendations_input.loc[
                    (user_recommendations_input["UID"] == uid)
                    & (
                        user_recommendations_input["Scholarship"]
                        == recommended_scholarship
                    )
                ]
            )
            > 0
        ):
            return False, str(
                "Already reviewed student " + str(uid) + " for this scholarship"
            )
        # Check here if students meets requirements of scholarship (Need to wait to merge Austin's PR before these)
        new_recommendations = new_recommendations.append(
            new_recommendation, ignore_index=True
        )
    # Check here for it too many recommendations for that scholarship, should be none if unlimited
    user_recommendations_input = user_recommendations_input.append(new_recommendations)
    user_recommendations_input.to_excel(
        get_appdata_path(f"/data/{SHAREPOINT.get_hawk_id()}_Reviews.xlsx"),
        index=False,
    )

    SHAREPOINT.upload(f"/data/{SHAREPOINT.get_hawk_id()}_Reviews.xlsx", "/data/")

    return True, user_recommendations_input


def main_view():
    """
    Main view shown when data is downloaded
    """
    if "students" not in st.session_state:
        SESSION.set_view("error")

    students = st.session_state.students
    current_data = students.copy()

    user_recommendations = st.session_state.user_recommendations
    scholarships = st.session_state.scholarships

    # Selecting a scholarship to use for filtering and reviews
    current_scholarship = st.selectbox(
        "Which scholarship would you like to consider?",
        np.append(["None"], scholarships["Name"].values),
    )
    if current_scholarship != "None":
        # Adding previos reviews to current data
        current_data_reviews = []
        for index, row in current_data.iterrows():
            student_recommendation = user_recommendations.loc[
                (user_recommendations["UID"] == row["UID"])
                & (user_recommendations["Scholarship"] == current_scholarship)
            ]
            if len(student_recommendation) > 0:
                current_data_reviews.append(student_recommendation["Rating"].iloc[0])
            else:
                current_data_reviews.append("N/A")
        current_data["Review"] = current_data_reviews

        # Filtering current data with scholarship criteria
        criteria = scholarships.loc[scholarships["Name"] == current_scholarship]
        groups_columns = []
        criteria_no_groups = []
        for column in criteria.columns.tolist():
            if column[0:5] == "Group":
                if (
                    isinstance(criteria[column].iloc[0], str)
                    and criteria[column].iloc[0].startswith("[")
                    and criteria[column].iloc[0].endswith("]")
                ):
                    groups_columns.append(
                        groups_string_to_list(criteria[column].iloc[0])
                    )
            elif column not in ["Name", "Total Amount", "Value"]:
                criteria_no_groups.append(column)
        for criterion in criteria_no_groups:
            if criterion in current_data.columns.tolist():
                try:
                    value = float(criteria[criterion])
                    in_group = False
                    for group in groups_columns:
                        if criterion in group:
                            in_group = True
                            met_criteria = False
                            for index, student in current_data.iterrows():
                                for group_c in group:
                                    if student[group_c] >= value:
                                        met_criteria = True
                                if met_criteria == False:
                                    current_data.drop(index)
                    if in_group == False:
                        current_data.drop(
                            current_data.loc[current_data[criterion] < value].index,
                            inplace=True,
                        )
                except ValueError:
                    value = criteria[criterion]
                    in_group = False
                    for group in groups_columns:
                        if criterion in group:
                            in_group = True
                            met_criteria = False
                            for index, student in current_data.iterrows():
                                for group_c in group:
                                    if student[group_c] >= value:
                                        met_criteria = True
                                if met_criteria == False:
                                    current_data.drop(index)
                    if in_group == False:
                        current_data.drop(
                            current_data.loc[current_data[criterion] != value].index,
                            inplace=True,
                        )

    # Configuring options for table functionality
    current_data.insert(0, "Select All", None)
    graph_data = GridOptionsBuilder.from_dataframe(current_data)
    graph_data.configure_pagination(enabled=True)  # Add pagination
    graph_data.configure_side_bar()  # Add a sidebar
    graph_data.configure_default_column(editable=False, groupable=True)
    graph_data.configure_selection(
        selection_mode="multiple", use_checkbox=True
    )  # Enable multi-row selection
    graph_data.configure_column("Select All", headerCheckboxSelection=True)
    graph_data.configure_grid_options(onFirstDataRendered=js)
    graph_data.configure_column(
        "Describe any relevant life experience related to engineering. ",
        onCellClicked=JsCode(
            "function(params) { alert(params.node.data['Describe any relevant life experience related to engineering. ']); };"
        ),
    )
    gridoptions = graph_data.build()
    gridoptions["getRowStyle"] = jscode
    custom_css = {}

    # Building the table
    grid_table = AgGrid(
        current_data,
        gridOptions=gridoptions,
        theme="balham",
        custom_css=custom_css,
        height=700,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        allow_unsafe_jscode=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
    )

    # Displaying statistics about main data frame
    main_data_statistics(current_data, students, grid_table)

    # Actions for user to take on main data frame
    with st.container():
        col1, col2, col3 = st.columns(3)

        # Submitting recommendations for scholarhsips
        with col1:
            with st.expander("Review Selected Students"):
                if current_scholarship == "None":
                    st.error("Must Select a Scholarship to Review For")
                else:
                    with st.form("recommendation_form"):
                        st.write(f"Review for Scholarship: {current_scholarship}")
                        rating = st.selectbox(
                            "Would you recommend these students for this scholarship?",
                            ["Yes", "No", "Maybe"],
                        )
                        additional_feedback = st.text_area(
                            "Enter any additional feedback on students"
                        )
                        submit_recommendation = st.form_submit_button(
                            "Submit Recommendation"
                        )
                        if "review_success" in st.session_state:
                            if st.session_state.review_success == "success":
                                st.success("Successfuly submitted recommendations!")
                                st.session_state["review_success"] = None
                            if st.session_state.review_success == "error":
                                st.error(st.session_state.review_result)
                                st.session_state["review_success"] = None
                        if submit_recommendation:
                            success, result = submit_recommendations(
                                user_recommendations,
                                current_scholarship,
                                rating,
                                additional_feedback,
                                grid_table,
                            )
                            if success is True:
                                st.session_state.user_recommendations = result
                                st.session_state.review_success = "success"
                                st.experimental_rerun()
                            else:
                                st.session_state.review_success = "error"
                                st.session_state.review_result = result
                                st.experimental_rerun()

        # Viewing graphs of student distributions
        with col2:
            with st.expander("See Distribution of Students"):
                with st.container():
                    numeric_cols = (
                        current_data.copy().select_dtypes(include="number").columns
                    )

                    fig_select1a = st.selectbox("Select X axis", numeric_cols.values)
                    fig_select1b = st.selectbox("Select Y axis", numeric_cols.values)
                    fig_select1c = st.selectbox(
                        "Highlight Scheme", ["None", "Selected Students"]
                    )  # , 'Scholarship Status'
                    show_legend = st.checkbox("Show Legend", True)
                    weight_bins = st.checkbox("Weight Plot", True)
                    sel_row_indices = None
                    if fig_select1c == "Selected Students":
                        sel_rows = grid_table["selected_rows"]
                        sel_row_indices = [
                            rows["_selectedRowNodeInfo"]["nodeRowIndex"]
                            for rows in sel_rows
                        ]
                    option_select = [show_legend, weight_bins, fig_select1c]
                    dynamic_fig(
                        current_data,
                        fig_select1a,
                        fig_select1b,
                        option_select,
                        sel_row_indices,
                    )  # Exporting the selected students
        with col3:
            if st.button("Export Current Table"):
                grid_table["data"].to_excel(
                    get_appdata_path("./data/Exported_Data.xlsx")
                )
                st.success("Exported data to /data as Exported_Data.xlsx")


if SESSION.view == "main":
    main_view()
elif SESSION.view == "error":
    error_view()
else:
    downloading_data_view()
