![Banner](https://github.com/stellaryx-labs/project-inferno/blob/main/captures/banner.png?raw=true)

Project Inferno is a data processing and visualization pipeline that uses NASA’s publicly available satellite remote sensing datasets to analyze wildfire extent and severity. By leveraging MODIS and VIIRS sensor data from FIRMS and EarthData Search, the pipeline extracts spectral band information, applies quality masks, and computes indices such as NBR, dNBR, and RdNBR to generate detailed burn severity maps.

- Fire mapping with NASA satellite remote sensing data  
- Severity analysis via algorithms calculating NBR, dNBR, and RdNBR  
- Visualizations showcasing fire dynamics  

**Read the Article**: 

## Project Showcase 
![Feature 1](https://github.com/stellaryx-labs/project-inferno/blob/main/captures/feature_1.png)

![Feature 2](https://github.com/stellaryx-labs/project-inferno/blob/main/captures/masking_display.png)

## Technologies Used
- **Python** for data processing and analysis  
- **Streamlit** for interactive web apps  
- **GDAL** and **Rasterio** for geospatial data handling  
- **Geopandas** for spatial data manipulation  
- **PyHDF** for HDF file handling
- **Plotly** for interactive visualizations
- **Numpy** for numerical operations and vectorization with ND arrays
- **Pandas** for data manipulation and analysis
- **autopep8** for code formatting and PEP8 compliance

## Data Sources
- [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/usfs/map/) — fire mapping data  
- [NASA EarthData Search](https://search.earthdata.nasa.gov/) — HDF files  

## Instructions and Bootstrapping

### Activate Virtual Environment using `conda`
```bash
conda init
conda create --name inferno
conda install -c conda-forge gdal libgdal-hdf python-kaleido
conda activate inferno
```

### Installation using `pip`
```bash
pip install streamlit plotly numpy pyhdf
pip install GDAL osgeo gdal kaleido
```

### Project File Outline
1. Streamlit Application
   - `config.py`: application configuration
   - `app.py`: main application logic
   - `pages/*.py`: individual UI components
   - `firms.py`: NASA FIRMS API integration

2. Data Processing Scripts
   - `hdf_extraction.py`: extract HDF metadata
   - `MCD64A1_date_extraction.py`: extract burn date & uncertainty
   - `data_masking.py`: apply bitmask to spectral bands
   - `dnbr_rdnbr_calc.py`: compute spectral indices & create char

### Usage 
```bash
chmod +x run_inferno_pipeline.sh
./run_inferno_pipeline.sh
```

**WARNING!**: this could take up to 30 minutes to run, depending on the specs of you system
## Sensor Synopsis

#### MODIS
- **Platforms**: Terra and Aqua
- **Spatial**: 250 m, 500 m, 1000 m
- **Spectral**: 36 bands (0.4 µm – 14.4 µm)
- **Temporal**: 1–2 days

#### VIIRS
- **Platforms**: NOAA 20, NOAA 21, Suomi NPP
- **Spatial**: 375 m, 750 m
- **Spectral**: 22 bands (0.402 µm – 12.49 µm)
- **Temporal**: Daily

## Data from Sensor Configurations
#### Shapefile Files  (GEOJSON)
- Eaton Perimeter: `datasets/Eaton_Perimeter_20250121.geojson`
- Palisades Perimeter: `datasets/Palisades_Perimeter_20250121.geojson`

#### CSV Files 
- **MODIS:** `firms_data/MODIS_C61.csv` — wide-area fire detection  
- **VIIRS J1:** `firms_data/J1_VIIRS_C2.csv` — 375m, NOAA-20  
- **VIIRS J2:** `firms_data/J2_VIIRS_C2.csv` — 375m, NOAA-21  
- **VIIRS Suomi:** `firms_data/SUOMI_VIIRS_C2.csv` — 375m, Suomi NPP  
- **LANDSAT:** `firms_data/LANDSAT.csv` — 30m, post-burn  

#### HDF Files
- **MCD64A1A**: Burned Area Monthly L3 Global 500m  
- **MOD09A1**: Terra Vegetation Indices 16-Day L3 Global 500m  
- **MYD09A1**: Aqua Vegetation Indices 16-Day L3 Global 500m  

#### Cleaned Bands
- MODIS: `data_processing/MOD09A1/cleaned_bands/`  
- MYD09A1: `data_processing/MYD09A1/cleaned_bands/`  

#### Visualizations
- `data_processing/visualizations/dnbr_visualization.html`: dNBR fire severity  
- `data_processing/visualizations/RdNBR_mod_over_time.html`: RdNBR over time (MODIS)  
- `data_processing/visualizations/RdNBR_myd_over_time.html`: RdNBR over time (MYD09A1)  
- `data_processing/visualizations/dnbr_mod_over_time.html`: dNBR over time (MODIS)  
- `data_processing/visualizations/dnbr_myd_over_time.html`: dNBR over time (MYD09A1)  
- `data_processing/visualizations/dnbr_aggregated.html`: Aggregated dNBR  

#### Future Features
- Add traceability to the pipeline (to keep track of data lineage): look into the [trace](https://docs.python.org/3/library/trace.html) library
- Add more visualizations for fire dynamics (esp for dNBR and RdNBR)

