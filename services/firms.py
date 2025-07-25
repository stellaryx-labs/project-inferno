# Data to analyze the NASA FIRMS fire data
import pandas as pd

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
PROCESS NASA FIRMS DATA AND THEN OVERLAY THE ANALYSIS FOR EACH OF THE FOLLOWING SENSOR CONFIGS
    -> MODIS        // [ firms_data/MODIS_C61.csv ]       -> legacy wide-area fire detection (1km/500m resolution)
    -> VIIRS J1     // [ firms_data/J1_VIIRS_C2.csv ]     -> 375m high-res thermal fire detection (NOAA-20)
    -> VIIRS J2     // [ firms_data/J2_VIIRS_C2.csv ]     -> 375m high-res thermal fire detection (NOAA-21)
    -> VIIRS Suomi  // [ firms_data/SUOMI_VIIRS_C2.csv ]  -> 375m fire detection from Suomi NPP satellite
    -> LANDSAT      // [ firms_data/LANDSAT.csv ]         -> 30m resolution for detailed post-burn and land change analysis
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def print_analytics():
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