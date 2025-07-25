import streamlit as st
import os
import sys
from services.firms import print_analytics, print_subset_info, get_timezone_for_location, print_california_timezones, subset_palisades_data, subset_eaton_data, convert_timezone_for_dataset
from pages.home import display_home
from config import TIMEZONE

# ENV SETUP: look into and find the proper commands for setting env variables
os.environ['GDAL_DATA'] = os.path.join(f'{os.sep}'.join(sys.executable.split(os.sep)[:-1]), 'Library', 'share', 'gdal')

st.set_page_config(
    page_title="PyroMap",
    page_icon="🔥",
    layout="centered"
)

st.title("2025 Eaton / Palisades Fires")

# Create three tabs
tab1, tab2, tab3 = st.tabs(["Fire Map", "Fire Severity Classification", "Thermal Signature Fingerprinting", "Most Dangerous Fires", "Fire Spread Estimator"])

with tab1:
    display_home()

with tab2:
    st.write("Content for the Eaton tab.")

with tab3:
    st.write("Content for the Palisades tab.")