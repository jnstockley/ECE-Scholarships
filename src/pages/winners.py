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
from src.utils.scholarship_management import groups_string_to_list

# Default setting for Streamlit page
st.set_page_config(layout="wide")

# Log in protecting the home page
cookie = logged_in()

if not cookie:
   redirect("/Log In")

@st.cache_data
def download_data():

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

# Start of display
st.header("Export Scholarship Winners")

# Filter selection (Will want to implement this once we have example filters)
current_scholarship = st.selectbox("Which scholarship would you like to consider?", np.append(["None"], scholarships["Name"].values))

# Need to download all of the recommendations
# Need to match up scholarship and student id than add the value's of yes no and maybe
# Initialize as none, so maybe will put them on there, then filter out ones that are none or negative
# Then just sort by that column
# Then have number import and button to export