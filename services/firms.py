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
from timezonefinder import TimezoneFinder
from config import EATON_GEOJSON_PATH, PALISADES_GEOJSON_PATH

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
    palisades_gdf = gpd.read_file(PALISADES_GEOJSON_PATH)
    eaton_gdf = gpd.read_file(EATON_GEOJSON_PATH)
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
    palisades_fire_gdf = palisades_fire_gdf[palisades_fire_gdf.within(palisades_shape_gdf.unary_union)]
    return palisades_fire_gdf

def subset_eaton_data():
    eaton_data = obtain_specific_fire_data("MODIS")
    eaton_shape_gdf = obtain_shapefiles()["eaton"]
    eaton_fires_gdf = gpd.GeoDataFrame(
        eaton_data,
        geometry=gpd.points_from_xy(eaton_data['longitude'], eaton_data['latitude']),
        crs=eaton_shape_gdf.crs
    )
    eaton_fires_gdf = eaton_fires_gdf[eaton_fires_gdf.within(eaton_shape_gdf.unary_union)]
    return eaton_fires_gdf

# Timezone Localization
"""
    Converts the 'acq_date' column of the DataFrame to the specified timezone.

    Args:
        df (pd.DataFrame): The DataFrame containing fire data.
        timezone (str): The timezone to convert to.

    Returns:
        pd.DataFrame: DataFrame with 'acq_date' converted to the specified timezone.
"""
def convert_timezone_for_dataset(df, timezone):
    df['acq_datetime'] = pd.to_datetime(df['acq_date'] + ' ' + df['acq_time'].astype(str).str.zfill(4), format='%Y-%m-%d %H%M')
    df['acq_datetime'].dt.tz_localize('GMT').dt.tz_convert(timezone)
    return df

# PRINTING METHODS
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

def print_subset_info():
    palisades_fire_gdf = subset_palisades_data()
    eaton_fires_gdf = subset_eaton_data()

    print("Palisades Fire DataFrame Shape:", palisades_fire_gdf.shape)
    print("Eaton Fire DataFrame Shape:", eaton_fires_gdf.shape)

    print("Palisades Fire Sample \n", palisades_fire_gdf.head(1))
    print("Eaton Fire Sample \n", eaton_fires_gdf.head(1))

def print_california_timezones():
    for timezone in pytz.country_timezones['CA']:
        print(timezone)

# Find the timezone for a specific location
"""
    Returns the timezone for a given latitude and longitude.

    Args:
        latitude (float): Latitude of the location.
        longitude (float): Longitude of the location.

    Returns:
        str: Timezone name.
"""
def get_timezone_for_location(latitude, longitude):
    tf = TimezoneFinder()
    return tf.timezone_at(lat=latitude, lng=longitude)