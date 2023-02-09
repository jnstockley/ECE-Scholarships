'''
Main application homepage.
'''
import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    '''
    Load in Uber data to be displayed.

        Parameters:
            nrows (int): Number of rows of data to load
        
        Returns:
            uber_data (pd.Dataframe): Uber dataframe formatted
    '''
    def convert_lower(word):
        return str(word).lower()

    uber_data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = convert_lower
    uber_data.rename(lowercase, axis='columns', inplace=True)
    uber_data[DATE_COLUMN] = pd.to_datetime(uber_data[DATE_COLUMN])
    return uber_data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader(f"Map of all pickups at {hour_to_filter}:00")
st.map(filtered_data)
