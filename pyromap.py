import streamlit as st
import os
import sys
from services.firms import print_analytics, print_subset_info, get_timezone_for_location, print_california_timezones, subset_palisades_data, subset_eaton_data, convert_timezone_for_dataset
from pages.home import display_home
from pages.severity import display_severity
from pages.danger import display_danger
from pages.spread import display_spread

from config import TIMEZONE

# ENV SETUP: look into and find the proper commands for setting env variables
os.environ['GDAL_DATA'] = os.path.join(f'{os.sep}'.join(sys.executable.split(os.sep)[:-1]), 'Library', 'share', 'gdal')

st.set_page_config(
    page_title="PyroMap",
    page_icon="🔥",
    layout="centered"
)

st.title("2025 Eaton & Palisades Fire ML Analysis 🔥")

tab1, tab2, tab3, tab4 = st.tabs(["Fire Map 🗺️", "Severity Analysis 🔥", "Danger Assessment 🛑", "Fire Spread Prediction 🚒"])

with tab1:
    display_home()

with tab2:
    display_severity()

with tab3:
    display_danger()

with tab3:
    display_spread()