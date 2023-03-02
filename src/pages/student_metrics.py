import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.markdown("Student Metrics")
st.sidebar.markdown("Student Metrics")

def build_metrics_page(student_data):
    st.title('Student Metrics')
    student_select = st.selectbox("Select Student",["temp1,temp2,temp3"])
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('graph 1 here')
            fig, ax = plt.subplots()
            ax.hist(student_data[0], bins=20)
            st.pyplot(fig)
        with col2:
            st.write('graph 2 here')
            fig, ax = plt.subplots()
            ax.hist(student_data[1], bins=20)
            st.pyplot(fig)
        with col3:
            st.write('graph 3 here')
            fig, ax = plt.subplots()
            ax.hist(student_data[2], bins=20)
            st.pyplot(fig)
    return

arrs = [np.random.normal(1, 1, size=100),np.random.normal(1, 1, size=100),np.random.normal(1, 1, size=100)]
build_metrics_page(arrs)