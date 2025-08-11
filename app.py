import streamlit as st
import os
import sys
from pages.home import display_home
from pages.severity import display_severity
from pages.about import display_about

# ENV SETUP: look into and find the proper commands for setting env variables
os.environ['GDAL_DATA'] = os.path.join(f'{os.sep}'.join(
    sys.executable.split(os.sep)[:-1]), 'Library', 'share', 'gdal')

st.set_page_config(
    page_title="Project Inferno",
    page_icon="🔥",
    layout="centered"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Russo+One&display=swap');
    h2, h4, p {
        font-family: 'Russo One', monospace !important;
        font-weight: 500 !important;
        letter-spacing: 1.5px;
        color: #ff6600;
    }

    .description {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2>Project Inferno 🔥</h2>", unsafe_allow_html=True)
st.markdown(
    "<h4>Autonomous Geospatial Analytics for Wildfire Intelligence Using Open-Source EO Data</h4>",
    unsafe_allow_html=True)
st.markdown(
    "<p>Case Study: 2025 Eaton & Palisades Fires, California</p>",
    unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Fire Map 🗺️", "Severity Analysis 🔥", "About ℹ️"])

with tab1:
    display_home()

with tab2:
    display_severity()

with tab3:
    display_about()
