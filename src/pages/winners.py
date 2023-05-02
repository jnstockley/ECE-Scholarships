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
from src.utils.sharepoint import logged_in, download, upload, login, get_files
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

    files = get_files(creds)

    for file in files: 
        if file == "Select File":
            continue
        else:
            download(file, f"{os.getcwd()}/data/", creds)
    
    # Initialize data: 
    st.session_state.students = pd.read_excel("./data/Master_Sheet.xlsx")
    st.session_state.scholarships = pd.read_excel("./data/Scholarships.xlsx")
    directory = "./data"
    result = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        st.write("f:")
        st.write(f)
        if os.path.isfile(f):
            if 'Reviews.xlsx' in f: 
                result.append(pd.read_excel(f))
    st.session_state.all_recommendations = result


    return creds, hawk_id
    
creds, hawk_id = download_data()


# Setting variables

students = st.session_state.students

scholarships = st.session_state.scholarships

all_recommendations = st.session_state.all_recommendations

# Start of display
st.header("Export Scholarship Winners")



st.write(result)

#st.write(all_recommendations)

# Filter selection (Will want to implement this once we have example filters)
current_scholarship = st.selectbox("Which scholarship would you like to consider?", np.append(["None"], scholarships["Name"].values))

# Need to download all of the recommendations and store them in a list
# Loop through each dataframe in the list
# Need to match up scholarship and student id than add the value's of yes no and maybe
# Initialize as none, so maybe will put them on there, then filter out ones that are none or negative
# Then just sort by that column
# Then have number import and button to export