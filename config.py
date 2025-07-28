# config.py

from pathlib import Path

ROOT_DIR = Path(__file__).parent

LAT = 34.17028
LONG = -118.34667
TIMEZONE = "America/Los_Angeles"
COORDINATE_REFERENCE_SYSTEM = "EPSG:4326"
DEFAULT_SATELLITE = "MODIS"

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

# TODO: change the heatmap color range depending on the satellite data used
custom_config = {
    "version": "v1",
    "config": {
        "visState": {
            "layers": [
                    {
                    "id": "heatmap-layer",
                    "type": "heatmap",
                    "config": {
                        "dataId": "fire-data",
                        "label": "Fire Heatmap",
                        "colorField": None,
                        "colorScale": "heatmap",
                        "sizeField": None,
                        "sizeScale": "linear",
                        "visConfig": {
                            "opacity": 0.8,
                            "colorRange": {
                                "name": "Global Warming",
                                "type": "sequential",
                                "category": "Uber",
                                "colors": [
                                    "#5A1846", "#900C3F", "#C70039", "#E3611C", "#F1920E", "#FFC300"
                                ]
                            },
                            "radius": 20
                        },
                        "weightField": {
                          "name": "frp", # shows the intensity for the heatmap
                          "type": "real"
                        }
                    }
                },
                    {
                        "id": "eaton-perimeter",
                        "type": "polygon",
                        "config": {
                            "dataId": "eaton-perimeter",
                            "label": "Eaton Fire Perimeter",
                            "visConfig": {
                                "opacity": 0.1,  # Lower fill opacity
                                "strokeOpacity": 1,
                                "outline": True,
                                "outlineColor": [0, 0, 0],
                                "thickness": 2,
                                "stroked": True,
                                "filled": False,
                            }
                        }
                    },
                    {
                        "id": "palisades-perimeter",
                        "type": "polygon",
                        "config": {
                            "dataId": "palisades-perimeter",
                            "label": "Palisades Fire Perimeter",
                            "visConfig": {
                                "opacity": 0,  # Lower fill opacity
                                "strokeOpacity": 0.8,
                                "outline": True,
                                "outlineColor": [0, 0, 0],
                                "thickness": 2,
                                "stroked": True,
                                "filled": False,
                            }
                        }
                    }
            ]
        },
        "mapState": {
            "latitude": LAT,
            "longitude": LONG,
            "zoom": 10,
            "bearing": 0,
            "pitch": 0
        }
    }
}