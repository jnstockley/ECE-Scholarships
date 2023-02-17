'''
Main application homepage.
'''
import streamlit as st
import pandas as pd

st. set_page_config(layout="wide")

st.title('Review Applicants')

current_filter = st.selectbox("Which filter would you like to apply?",
                              ("Evan's custom filter", "Scholarship 1", "Scholarship 2"))

st.write("Current filter:", current_filter)

df = pd.read_excel("./tests/data/ece_scholarship_applicants.xlsx", nrows=15)
st.write("***Example With Actions")
colms = st.columns((1, 2, 1, 1, 1))
fields = ["UID", "Name", "Program", "Sex", "Review"]
for col, field_name in zip(colms, fields):
    col.write(field_name)

for x, uid in enumerate(df["UID"]):
    col1, col2, col3, col4, col5 = st.columns((1, 2, 1, 1, 1))
    col1.write(uid)
    col2.write(df["Name"][x])
    col3.write(df["Programs"][x])
    col4.write(df["Sex"][x])
    REVIEWED = False
    BUTTON_TYPE = "Review" if not REVIEWED else "Rereview"
    button_phold = col5.empty()  # create a placeholder
    do_action = button_phold.button(BUTTON_TYPE, key=x)
    if do_action:
        # do some action with a row's data
        button_phold.empty()  # remove button


st.write("***Example with Built In Table")
st.dataframe(df)

st.button("Export current data")
