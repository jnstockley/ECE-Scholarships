import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_fig(data, data_title, highlight=None):
    fig, ax = plt.subplots()
    n, bin1, patches = ax.hist(data, bins=20)
    if highlight is not None:
        patches[5].set_fc('red')
    plt.title(data_title)
    st.pyplot(fig)
    return fig, ax


def build_metrics_page(student_data, highlight_id=None):
    st.title('Student Metrics')
    student_select = st.selectbox("Select Student",["temp1","temp2","temp3"])
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('Graph 1')
            create_fig(student_data['ACT'], 'ACT', student_data['ACT'][5])
            create_fig(student_data['SAT'], 'SAT')
        with col2:
            st.write('Graph 2')
            create_fig(student_data['GPA'], 'GPA')
        with col3:
            st.write('Graph 3')
            create_fig(student_data['Financial Need'], 'Financial Need')
    return

#Assuming data is a dictionary

st.markdown("Student Metrics")
st.sidebar.markdown("Student Metrics")

data = {'GPA':np.random.normal(1, 1, size=100),
        'ACT':np.random.normal(1, 1, size=100),
        'SAT':np.random.normal(1, 1, size=100),
        'Financial Need':np.random.normal(1, 1, size=100)}
build_metrics_page(data)