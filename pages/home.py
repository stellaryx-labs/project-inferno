import streamlit as st
import geopandas as gpd
from keplergl import KeplerGl
import os
import sys
import pandas as pd

from config import custom_config, EATON_GEOJSON_PATH, PALISADES_GEOJSON_PATH

"""
Obtain all relevant fire data to be displayed within the home page of the Streamlit application
Return: <Dict> fields: {eaton <Str: JSON Str for Perimeter>, palisades <Str: JSON Str for Perimeter>}
"""
def _obtain_perimeter_data():
    # Install and Leverage the GEOJSON (perimeter) file for the 2025 Eaton Fire
    eaton_gdf = gpd.read_file(EATON_GEOJSON_PATH)
    eaton_json_str = eaton_gdf.to_json()

    palisades_gdf = gpd.read_file(PALISADES_GEOJSON_PATH)
    palisades_json_str = palisades_gdf.to_json()

    return {"eaton": eaton_json_str, "palisades": palisades_json_str}

"""

"""

"""
Main function to display the contents of the home page within the Streamlit application
"""
def display_home():
    # Set the origin of the map to the NADIR point
    perimeter_data = _obtain_perimeter_data()

    map_ = KeplerGl(height=600, config=custom_config)
    map_.add_data(data=perimeter_data["eaton"], name="2025 Eaton Fire")
    map_.add_data(data=perimeter_data["palisades"], name="2025 Palisades Fire")
    map_.save_to_html(file_name="../main_map.html")
    st.components.v1.html(open("main_map.html").read(), height=600, scrolling=True)


