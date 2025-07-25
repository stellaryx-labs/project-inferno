import streamlit as st
import os
import sys
from services.firms import print_analytics, subset_palisades_data, subset_eaton_data
from pages.home import display_home

# ENV SETUP: look into and find the proper commands for setting env variables
os.environ['GDAL_DATA'] = os.path.join(f'{os.sep}'.join(sys.executable.split(os.sep)[:-1]), 'Library', 'share', 'gdal')


st.set_page_config(
    page_title="PyroMap",
    page_icon="🔥",
    layout="centered"
)

st.title("2025 Eaton / Palisades Fires")

# Create three tabs
tab1, tab2, tab3 = st.tabs(["Main", "Eaton", "Palisades"])

with tab1:
    display_home()

with tab2:
    st.write("Content for the Eaton tab.")

with tab3:
    st.write("Content for the Palisades tab.")