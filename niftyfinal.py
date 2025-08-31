import pandas as pd
import streamlit as st
import numpy as np
header = st.header('Nifty View')
file = st.file_uploader(' please select your csv file' )
data = pd.read_csv(file, skiprows=1)
st.write(data)
st.write(data.columns.pop([0,23])














