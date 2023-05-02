# Importing packages
import os
import streamlit as st
import pandas as pd
import numpy as np
from src.utils.html import redirect
from src.utils.sharepoint import logged_in, download, login, get_files

# Default setting for Streamlit page
st.set_page_config(layout="wide")

# Log in protecting the page
cookie = logged_in()
if not cookie:
   redirect("/Log In")

# Downloading the data needed on first visit
@st.cache_data
def download_data():
    '''
    Caching credentials and downloads so only have to do on page load
    '''
    # Gathering login credentials
    creds = login(cookie)
    hawk_id = cookie.get('cred')['hawk-id']

    # Downloading needed data
    files = get_files(creds)
    for file in files: 
        if file == "Select File":
            continue
        else:
            if '/data/' in file:
                download(file, f"{os.getcwd()}/data/", creds)
    
    # Initializing session data
    st.session_state.students = pd.read_excel("./data/Master_Sheet.xlsx")
    st.session_state.scholarships = pd.read_excel("./data/Scholarships.xlsx")
    directory = "./data"
    result = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            if 'Reviews.xlsx' in f: 
                result.append(pd.read_excel(f))
    st.session_state.all_recommendations = result

    return creds, hawk_id

# Setting variables for script
creds, hawk_id = download_data()
students = st.session_state.students
current_data = students.copy()
scholarships = st.session_state.scholarships
all_recommendations = st.session_state.all_recommendations

# Start of display
st.header("Export Scholarship Winners")

# Scholarhsip selection
current_scholarship = st.selectbox("Which scholarship would you like to consider?", np.append(["None"], scholarships["Name"].values))

# Calculating vote scores for selected scholarship
current_data.insert(0, 'Vote Score', None)
for student_index, student in current_data.iterrows():
    for recommender in all_recommendations:
        for recommendation_index, recommendation in recommender.iterrows():
            if recommendation['UID'] == student['UID'] and recommendation['Scholarship'] == current_scholarship:
                if current_data.at[student_index, 'Vote Score'] == None:
                    current_data.at[student_index, 'Vote Score'] = 0
                if recommendation['Rating'] == "Yes":
                    current_data.at[student_index, 'Vote Score'] = current_data.at[student_index, 'Vote Score'] + 1
                elif recommendation['Rating'] == "No":
                    current_data.at[student_index, 'Vote Score'] = current_data.at[student_index, 'Vote Score'] - 1
                elif recommendation['Rating'] == "Maybe":
                    current_data.at[student_index, 'Vote Score'] = current_data.at[student_index, 'Vote Score']

# Dropping students that received no reviews or a negative vote Score
current_data = current_data[current_data['Vote Score'].notna()]
current_data.drop(current_data.loc[current_data['Vote Score'] < 0].index, inplace = True)
current_data = current_data.sort_values(by=['Vote Score'], ascending=False)

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
            current_data.to_excel('./data/Scholarship_Winners.xlsx')
            st.success('Exported data to /data! as Scholarship_Winners.xlsx')

    # Choose a number of top vote scorers to export
    with col2: 
        value = st.number_input('Number to export', min_value=0, step=1, label_visibility='collapsed')
    
    # Export the previously chosen number of top vote scorers 
    with col3: 
         if st.button(f"Export Top {value} Vote Getters for Scholarship"):
            current_data.iloc[:value].to_excel('./data/Scholarship_Winners.xlsx')
            st.success('Exported data to /data as Scholarship_Winners.xlsx')