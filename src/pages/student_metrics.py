import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math

def create_fig(data, data_title, highlight=None):
    highlight = highlight.values[0]
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(data, bins=20)
    if highlight is not None and not math.isnan(highlight):
        b = pd.cut([highlight],bins)
        if type(b[0]) != float:
            binc = np.where(abs(bins-b[0].left) < 0.001)
            binc = binc[0][0]
            patches[binc].set_fc('red')
    plt.title(data_title)
    st.pyplot(fig)
    return fig, ax


def build_metrics_page(data):
    st.title('Student Metrics')
    student_select = st.selectbox("Select Student",data['Name'])
    highlight_id = data[data['Name']==student_select].index.values
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('Graph 1')
            create_fig(data['ACT Composite Score'], 'ACT Composite', data['ACT Composite Score'][highlight_id])
        with col2:
            st.write('Graph 2')
            create_fig(data['Upcoming Financial Need After Grants/Scholarships'], 'Financial Need', data['Upcoming Financial Need After Grants/Scholarships'][highlight_id])
        with col3:
            st.write('Graph 3')
            create_fig(data['High School GPA'], 'High School GPA', data['High School GPA'][highlight_id])
    return

#Assuming data is a dictionary

st.markdown("Student Metrics")
st.sidebar.markdown("Student Metrics")
df = pd.read_excel("./tests/data/ece_scholarship_applicants.xlsx", nrows=15)
build_metrics_page(df)