import streamlit as st
import geopandas as gpd
from keplergl import KeplerGl
import os
import sys
import json

# ENV SETUP: look into and find the proper commands for setting env variables
os.environ['GDAL_DATA'] = os.path.join(f'{os.sep}'.join(sys.executable.split(os.sep)[:-1]), 'Library', 'share', 'gdal')

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

# Extract the NADIR point from the GeoDataFrame
nadir_point = eaton_gdf.geometry.centroid.iloc[0]
print(f"NADIR Point: {nadir_point}")

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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
0x01 > PROCESS NASA FIRMS DATA AND THEN OVERLAY THE ANALYSIS FOR EACH OF THE FOLLOWING SENSOR CONFIGS
    -> MODIS: legacy wide-area fire detection (1km/500m resolution)
    -> VIIRS J1: 375m high-res thermal fire detection (NOAA-20)
    -> VIIRS J2: 375m high-res thermal fire detection (NOAA-21)
    -> VIIRS Suomi: 375m fire detection from Suomi NPP satellite
    -> LANDSAT: 30m resolution for detailed post-burn and land change analysis
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


