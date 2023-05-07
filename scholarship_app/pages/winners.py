"""
Winners: A page for the admin to be able to export the scholarship winners after reviews have been completed
"""

# Importing packages
import os
import streamlit as st
import pandas as pd
import numpy as np
from scholarship_app.utils.html import redirect
from scholarship_app.utils.output import get_appdata_path
from scholarship_app.managers.sharepoint.sharepoint_session import SharepointSession

# Default setting for Streamlit page
st.set_page_config(layout="wide")

SHAREPOINT = SharepointSession(st.session_state)
if not SHAREPOINT.is_signed_in():
    redirect("/Account")

# Setting variables for script
with st.spinner("Downloading Data..."):
    if "students" not in st.session_state:
        SHAREPOINT.download("/data/Master_Sheet.xlsx", "/data/")
        st.session_state.students = pd.read_excel(
            get_appdata_path("/data/Master_Sheet.xlsx")
        )
    students = st.session_state.students
    current_data = students.copy()
    if "scholarships" not in st.session_state:
        SHAREPOINT.download("/data/Scholarships.xlsx", "/data/")
        st.session_state.scholarships = pd.read_excel(
            get_appdata_path("/data/Scholarships.xlsx")
        )
    scholarships = st.session_state.scholarships
    if "all_recommendations" not in st.session_state:
        files = SHAREPOINT.get_files()
        for file in files:
            if file == "Select File":
                continue
            if "/data/" in file and "reviews" in file and "/tests/" not in file:
                SHAREPOINT.download(file, "/data/")
        result = []
        DIRECTORY = ".app_data/data"
        for filename in os.listdir(DIRECTORY):
            file = os.path.join(DIRECTORY, filename)
            if os.path.isfile(file):
                if "Reviews.xlsx" in file:
                    result.append(pd.read_excel(file))
        st.session_state.all_recommendations = result
    all_recommendations = st.session_state.all_recommendations


# Start of display
st.header("Export Scholarship Winners")

# Scholarhsip selection
current_scholarship = st.selectbox(
    "Which scholarship would you like to consider?",
    np.append(["None"], scholarships["Name"].values),
)

# Calculating vote scores for selected scholarship
current_data.insert(0, "Vote Score", None)
for student_index, student in current_data.iterrows():
    for recommender in all_recommendations:
        for recommendation_index, recommendation in recommender.iterrows():
            if (
                recommendation["UID"] == student["UID"]
                and recommendation["Scholarship"] == current_scholarship
            ):
                if current_data.at[student_index, "Vote Score"] == None:
                    current_data.at[student_index, "Vote Score"] = 0
                if recommendation["Rating"] == "Yes":
                    current_data.at[student_index, "Vote Score"] = (
                        current_data.at[student_index, "Vote Score"] + 1
                    )
                elif recommendation["Rating"] == "No":
                    current_data.at[student_index, "Vote Score"] = (
                        current_data.at[student_index, "Vote Score"] - 1
                    )
                elif recommendation["Rating"] == "Maybe":
                    current_data.at[student_index, "Vote Score"] = current_data.at[
                        student_index, "Vote Score"
                    ]

# Dropping students that received no reviews or a negative vote Score
current_data = current_data[current_data["Vote Score"].notna()]
current_data.drop(current_data.loc[current_data["Vote Score"] < 0].index, inplace=True)
current_data = current_data.sort_values(by=["Vote Score"], ascending=False)

# Giving feedback if no scholarship selected
if current_scholarship == "None":
    st.error("Select a Scholarship")

# Displaying students that received a vote score >= 0
st.write(current_data)

# Actions for user to take on current data
with st.container():
    col1, col2, col3 = st.columns(3)

    # Export all students that received a vote score >= 0
    with col1:
        if st.button("Export All Vote Getters for Scholarship"):
            current_data.to_excel(get_appdata_path("/data/Scholarship_Winners.xlsx"))
            st.success("Exported data to /data! as Scholarship_Winners.xlsx")

    # Choose a number of top vote scorers to export
    with col2:
        value = st.number_input(
            "Number to export", min_value=0, step=1, label_visibility="collapsed"
        )

    # Export the previously chosen number of top vote scorers
    with col3:
        if st.button(f"Export Top {value} Vote Getters for Scholarship"):
            current_data.iloc[:value].to_excel(
                get_appdata_path("/data/Scholarship_Winners.xlsx")
            )
            st.success("Exported data to /data as Scholarship_Winners.xlsx")
