#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 22:46:03 2024

@author: abdulzaf
"""

import streamlit as st
import pandas as pd
import numpy as np

DATA_URL = '../export/2024_2025/compilation_sherbrooke.csv'

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_URL)
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

st.subheader('Raw data')
st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data.CVE)[0]

st.bar_chart(hist_values)
