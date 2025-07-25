import streamlit as st
import geopandas as gpd
from keplergl import KeplerGl
import os
import sys
import pandas as pd


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
0x00 > START BY PROCESSING PERIMETER DATA AND DISPLAYING IT ONTO A STREAMLIT APP
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# Install and Leverage the GEOJSON (perimeter) file for the 2025 Eaton Fire
eaton_gdf = gpd.read_file("./datasets/Eaton_Perimeter_20250121.geojson")
print(type(eaton_gdf))
eaton_json_str = eaton_gdf.to_json()
print(eaton_json_str)

palisades_gdf = gpd.read_file("./datasets/Palisades_Perimeter_20250121.geojson")
palisades_json_str = palisades_gdf.to_json()

# Set the origin of the map to the NADIR point
custom_config = {
    "mapState": {
        "latitude": 34.17028,  # Default latitude
        "longitude": -118.34667,  # Default longitude
        "zoom": 9,  # Default zoom level
        "bearing": 0,
        "pitch": 0,
    }
}

map_ = KeplerGl(height=600, config=custom_config)
map_.add_data(data=eaton_json_str, name="2025 Eaton Fire")
map_.add_data(data=palisades_json_str, name="2025 Palisades Fire")

# Save and display
map_.save_to_html(file_name="eaton_map.html")
st.components.v1.html(open("eaton_map.html").read(), height=600, scrolling=True)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
0x01 > PROCESS NASA FIRMS DATA AND THEN OVERLAY THE ANALYSIS FOR EACH OF THE FOLLOWING SENSOR CONFIGS
    -> MODIS        // [ firms_data/MODIS_C61.csv ]       -> legacy wide-area fire detection (1km/500m resolution)
    -> VIIRS J1     // [ firms_data/J1_VIIRS_C2.csv ]     -> 375m high-res thermal fire detection (NOAA-20)
    -> VIIRS J2     // [ firms_data/J2_VIIRS_C2.csv ]     -> 375m high-res thermal fire detection (NOAA-21)
    -> VIIRS Suomi  // [ firms_data/SUOMI_VIIRS_C2.csv ]  -> 375m fire detection from Suomi NPP satellite
    -> LANDSAT      // [ firms_data/LANDSAT.csv ]         -> 30m resolution for detailed post-burn and land change analysis
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

modis_df = pd.read_csv('./firms_data/MODIS_C61.csv')
viirs_j1_df = pd.read_csv('./firms_data/J1_VIIRS_C2.csv')
viirs_j2_df = pd.read_csv('./firms_data/J2_VIIRS_C2.csv')
viirs_suomi_df = pd.read_csv('./firms_data/SUOMI_VIIRS_C2.csv')
landsat_df = pd.read_csv('./firms_data/LANDSAT.csv')

print("MODIS DataFrame Shape:", modis_df.shape)
print("VIIRS J1 DataFrame Shape:", viirs_j1_df.shape)
print("VIIRS J2 DataFrame Shape:", viirs_j2_df.shape)
print("VIIRS Suomi DataFrame Shape:", viirs_suomi_df.shape)
print("Landsat DataFrame Shape:", landsat_df.shape)

print("MODIS Sample \n", modis_df.head(1))
print("VIIRS J1 Sample \n", viirs_j1_df.head(1))
print("VIIRS J2 Sample \n", viirs_j2_df.head(1))
print("VIIRS Suomi Sample \n", viirs_suomi_df.head(1))
print("Landsat Sample \n", landsat_df.head(1))