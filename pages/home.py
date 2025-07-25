import streamlit as st
import geopandas as gpd
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static

from config import custom_config, EATON_GEOJSON_PATH, PALISADES_GEOJSON_PATH, HOME_PAGE_PATH
from services.firms import subset_eaton_data, subset_palisades_data, convert_timezone_for_dataset
from config import TIMEZONE, COORDINATE_REFERENCE_SYSTEM

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
Obtain the localized fire data for the 2025 Eaton and Palisades Fires
Return: Pandas DataFrame containing the localized fire data for both fires
"""
def _obtain_localized_fire_data():
    eaton_subset = subset_eaton_data()
    print("ss", eaton_subset["acq_date"].dtype)
    localized_eaton_subset = convert_timezone_for_dataset(eaton_subset, TIMEZONE)
    print(eaton_subset["acq_date"].dtype)
    palisades_subset = subset_palisades_data()
    localized_palisades_subset = convert_timezone_for_dataset(palisades_subset, TIMEZONE)
    return {
        "eaton": localized_eaton_subset,
        "palisades": localized_palisades_subset
    }

def _convert_dataframe_to_geopandas(df):
    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs=COORDINATE_REFERENCE_SYSTEM
    )
    return gdf

"""
Main function to display the contents of the home page within the Streamlit application
"""
def display_home():
    # Set the origin of the map to the NADIR point
    perimeter_data = _obtain_perimeter_data()
    fire_subset_data = _obtain_localized_fire_data()
    gpd_eaton_points = _convert_dataframe_to_geopandas(fire_subset_data["eaton"])
    gpd_palisades_points = _convert_dataframe_to_geopandas(fire_subset_data["palisades"])

    map_ = KeplerGl(height=600, config=custom_config)
    map_.add_data(data=perimeter_data["eaton"], name="2025 Eaton Fire")
    map_.add_data(data=perimeter_data["palisades"], name="2025 Palisades Fire")

    print("Eaton Fire Data:", gpd_eaton_points.head())
    # Plot the localized fire data for both fires using geopoints
    # map_.add_data(data=gpd_eaton_points, name="Localized Eaton Fire Data")
    # map_.add_data(data=gpd_palisades_points, name="Localized Palisades Fire Data")

    keplergl_static(
        map_,
        height=600,
        width=800,
        center_map=True,
        config=custom_config,
        use_container_width=True
    )



