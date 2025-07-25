# config.py

from pathlib import Path

ROOT_DIR = Path(__file__).parent

### ALL RELEVANT DATA PATHS AND CONFIGURATIONS FOR THE PYROMAP STREAMLIT APP ###
EATON_GEOJSON_PATH = ROOT_DIR / "datasets" / "Eaton_Perimeter_20250121.geojson"
PALISADES_GEOJSON_PATH = ROOT_DIR / "datasets" / "Palisades_Perimeter_20250121.geojson"

MODIS_DATA_PATH = ROOT_DIR / "firms_data" / "MODIS_C61.csv"
VIIRS_J1_DATA_PATH = ROOT_DIR / "firms_data" / "J1_VIIRS_C2.csv"
VIIRS_J2_DATA_PATH = ROOT_DIR / "firms_data" / "J2_VIIRS_C2.csv"
VIIRS_SUOMI_DATA_PATH = ROOT_DIR / "firms_data" / "SUOMI_VIIRS_C2.csv"
LANDSAT_DATA_PATH = ROOT_DIR / "firms_data" / "LANDSAT.csv"

# STREAMLIT PAGES
HOME_PAGE_PATH = ROOT_DIR / "main_map.html"
PALISADES_PATH = ROOT_DIR / "palisades.html"
EATON_PATH = ROOT_DIR / "eaton.html"

custom_config = {
    "mapState": {
        "latitude": 34.17028,  # Default latitude
        "longitude": -118.34667,  # Default longitude
        "zoom": 9,  # Default zoom level
        "bearing": 0,
        "pitch": 0,
    }
}
