"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
PROCESS NASA FIRMS DATA AND THEN OVERLAY THE ANALYSIS FOR EACH OF THE FOLLOWING SENSOR CONFIGS
    -> MODIS        // [ firms_data/MODIS_C61.csv ]       -> legacy wide-area fire detection (1km/500m resolution)
    -> VIIRS J1     // [ firms_data/J1_VIIRS_C2.csv ]     -> 375m high-res thermal fire detection (NOAA-20)
    -> VIIRS J2     // [ firms_data/J2_VIIRS_C2.csv ]     -> 375m high-res thermal fire detection (NOAA-21)
    -> VIIRS Suomi  // [ firms_data/SUOMI_VIIRS_C2.csv ]  -> 375m fire detection from Suomi NPP satellite
    -> LANDSAT      // [ firms_data/LANDSAT.csv ]         -> 30m resolution for detailed post-burn and land change analysis
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Data to analyze the NASA FIRMS fire data
import pandas as pd
import geopandas as gpd
from config import MODIS_DATA_PATH, VIIRS_J1_DATA_PATH, VIIRS_J2_DATA_PATH, VIIRS_SUOMI_DATA_PATH, LANDSAT_DATA_PATH
import pytz

def print_analytics():
    modis_df = pd.read_csv(MODIS_DATA_PATH)
    viirs_j1_df = pd.read_csv(VIIRS_J1_DATA_PATH)
    viirs_j2_df = pd.read_csv(VIIRS_J2_DATA_PATH)
    viirs_suomi_df = pd.read_csv(VIIRS_SUOMI_DATA_PATH)
    landsat_df = pd.read_csv(LANDSAT_DATA_PATH)

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


"""
Fetches the fire data from the specified CSV files and returns them as pandas DataFrames.

Returns:
    dict: A dictionary containing DataFrames for each fire data source.
"""
def obtain_all_fire_data():
    fire_data = {
        "MODIS": pd.read_csv(MODIS_DATA_PATH),
        "VIIRS_J1": pd.read_csv(VIIRS_J1_DATA_PATH),
        "VIIRS_J2": pd.read_csv(VIIRS_J2_DATA_PATH),
        "VIIRS_Suomi": pd.read_csv(VIIRS_SUOMI_DATA_PATH),
        "LANDSAT": pd.read_csv(LANDSAT_DATA_PATH)
    }
    return fire_data

"""
Fetches specific fire data based on the sensor type.
Args:
    sensor_type (str): The type of sensor data to fetch (e.g., "MODIS", "VIIRS_J1", etc.).
"""
def obtain_specific_fire_data(sensor_type):
    fire_data = obtain_all_fire_data()
    if sensor_type in fire_data:
        return fire_data[sensor_type]
    else:
        raise ValueError(f"Sensor type '{sensor_type}' not found in the fire data.")

"""
Fetches the shapefile data for the fire data sources and returns them as GeoDataFrames.

Returns:
    dict: A dictionary containing GeoDataFrames for each fire data source.
"""
def obtain_shapefiles():
    palisades_gdf = gpd.read_file(states_shapefile_url)
    eaton_gdf = gpd.read_file(states_shapefile_url)
    return {
        "palisades": palisades_gdf,
        "eaton": eaton_gdf
    }

# Subsetting functions for Eaton and Palisades data
def subset_palisades_data():
    palisades_data = obtain_specific_fire_data("MODIS")
    palisades_shape_gdf = obtain_shapefiles()["palisades"]
    palisades_fire_gdf = gpd.GeoDataFrame(
        palisades_data,
        geometry=gpd.points_from_xy(palisades_data['longitude'], palisades_data['latitude']),
        crs=palisades_shape_gdf.crs
    )
    return palisades_fire_gdf

def subset_eaton_data():
    eaton_data = obtain_specific_fire_data("MODIS")
    eaton_shape_gdf = obtain_shapefiles()["eaton"]
    eaton_fires_gdf = gpd.GeoDataFrame(
        eaton_data,
        geometry=gpd.points_from_xy(eaton_data['longitude'], eaton_data['latitude']),
        crs=eaton_shape_gdf.crs
    )
    return eaton_fires_gdf

# Timezone Localization

def convert_datetime_to_timezone(dt, timezone):
    """
    Converts a datetime object to the specified timezone.

    Args:
        dt (datetime): The datetime object to convert.
        timezone (str): The timezone to convert to (e.g., 'America/Los_Angeles').

    Returns:
        datetime: The converted datetime object in the specified timezone.
    """
    tz = pytz.timezone(timezone)
    return dt.astimezone(tz)

def print_california_timezones():
    for timeZone in pytz.country_timezones['CA']:
        print(timeZone)