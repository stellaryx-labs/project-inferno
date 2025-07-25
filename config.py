# config.py

### ALL RELEVANT DATA PATHS AND CONFIGURATIONS FOR THE PYROMAP STREAMLIT APP ###
EATON_GEOJSON_PATH = "./datasets/Eaton_Perimeter_20250121.geojson"
PALISADES_GEOJSON_PATH = "./datasets/Palisades_Perimeter_20250121.geojson"

custom_config = {
    "mapState": {
        "latitude": 34.17028,  # Default latitude
        "longitude": -118.34667,  # Default longitude
        "zoom": 9,  # Default zoom level
        "bearing": 0,
        "pitch": 0,
    }
}
