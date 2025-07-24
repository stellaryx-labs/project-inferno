# PyroMap

### Instructions and Bootstrapping
```
conda init
conda create --name pyromap
conda activate pyromap
```

### Scope of this Project // include a dashboard to contain all of the following... 
- Data Analysis and Visualization of the Fire Data 
- Fire Severity Classification
- Thermal Signature Fingerprinting
- Most Dangerous Fires // take into consideration population density, proximity to cities, infrastructure damage, and other factors
- Predictive Fire Spread Estimator

SCOPE THE Project to the Palisades Fires within Los Angeles, California 

- Article to Introduce Beginners to the Project // How to use the NASA FIRMS API

### Libraries 
- pandas

### Datasets
Fire Information for Resource Management System

### Instruments
- MODIS (Moderate Resolution Imaging Spectroradiometer) // Aqua and Terra
- VIIRS (Visible Infrared Imaging Radiometer Suite) // Suomi NPP and NOAA-20 and NOAA-21

Available within 3 hrs of satellite observation

### User Interface of FIRMS NASA 

### Dataset Information Retrieval

VIIRS I-Band 375m Active Fire Data
- provides a greater response over fires of relatively small areas
- provides improved mapping of large fire perimeters
- enhanced nighttime performance

### Dataset Distribution Titles 
https://www.earthdata.nasa.gov/data/instruments/viirs/viirs-i-band-375-m-active-fire-data

- Latitude: lat of center of nominal 375m fire pixel
- Longitude: lon of center of nominal 375m fire pixel
- Bright_ti4: VIIRS I-4 channel brightness temperature of the fire pixel measured in Kelvin
- Scan: Along Scan pixel size... algorithm produces 375 m pixels at the nadir (center) of the scan
- Track: Along Track pixel size... algorithm produces 375 m pixels at the nadir (center) of the scan
- Acq_Date: Date of acquisition in UTC
- Acq_Time: Time of acquisition in UTC
- Satellite: Satellite platform
- Confidence: Confidence level of the fire detection.. quality of the pixel
  - sun glint: low confidence
  - low rel temp anamoly: low confidence
- Version: collection and source of data processing
- Bright_ti5: VIIRS I-5 channel brightness temperature of the fire pixel measured in Kelvin
- FRP (Fire Radiative Power): Fire Radiative Power in MW
- Day_Night: Day or Night observation

### Regional Coordinates 

- **World**: West: -180, South: -90, East: 180, North: 90
- **Canada**: West: -150, South: 40, East: -49, North: 79
- **Alaska**: West: -180, South: 50, East: -139, North: 72
- **USA (Conterminous) & Hawaii**: West: -160.5, South: 17.5, East: -63.8, North: 50
- **Central America**: West: -119.5, South: 7, East: -58.5, North: 33.5
- **South America**: West: -112, South: -60, East: -26, North: 13
- **Europe**: West: -26, South: 34, East: 35, North: 82
- **North and Central Africa**: West: -27, South: -10, East: 52, North: 37.5
- **Southern Africa**: West: 10, South: -36, East: 58.5, North: -4
- **Russia and Asia**: West: 26, South: 9, East: 180, North: 83.5
- **South Asia**: West: 54, South: 5.5, East: 102, North: 40
- **South East Asia**: West: 88, South: -12, East: 163, North: 31
- **Australia and New Zealand**: West: 110, South: -55, East: 180, North: -10

### Dataset Information
As you may have seen when looking at data_availability there are following available datasets:

- LANDSAT_NRT **US/Canada only** [data attributes](https://www.earthdata.nasa.gov/data/tools/firms/faqs)
- MODIS_NRT [data attributes](https://www.earthdata.nasa.gov/learn/find-data/near-real-time/firms/mcd14dl-nrt#ed-firms-attributes)
- MODIS_SP [data attributes](https://www.earthdata.nasa.gov/learn/find-data/near-real-time/firms/mcd14dl-nrt#ed-firms-attributes)
- VIIRS_NOAA20_NRT [data attributes](https://www.earthdata.nasa.gov/learn/find-data/near-real-time/firms/vnp14imgtdlnrt#ed-viirs-375m-attributes)
- VIIRS_SNPP_NRT [data attributes](https://www.earthdata.nasa.gov/learn/find-data/near-real-time/firms/vnp14imgtdlnrt#ed-viirs-375m-attributes)
- VIIRS_SNPP_SP [data attributes](https://www.earthdata.nasa.gov/learn/find-data/near-real-time/firms/vnp14imgtdlnrt#ed-viirs-375m-attributes)

**NRT**: dataset consists of (Near Real-Time, Real-Time and Ultra Real-Time) data. [view details on RT and URT](https://www.earthdata.nasa.gov/data/tools/firms/faq). Also explore our blog: [Wildfire detection in the US and Canada within a minute of satellite observation](https://wiki.earthdata.nasa.gov/display/FIRMS/2022/07/14/Wildfire+detection+in+the+US+and+Canada+within+a+minute+of+satellite+observation)

**SP**: Standard Processing; standard data products are an internally consistent, well-calibrated record of the Earth’s geophysical properties to support science. There is a multi-month lag in this dataset availability. [more information on SP vs NRT](https://www.earthdata.nasa.gov/data/tools/firms/faq)

### Subsetting using Polygons
This shapefile is from [this](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html) 
https://www.census.gov/geographies/mapping-files.html

# TODO
https://firms.modaps.eosdis.nasa.gov/academy
- [x] Data Ingestion and Manipulation
- [x] Using FIRMS API
- [x] Data Visualization
- [x] Data Subsetting

- finish all of the FIRMS videos
- finish all of the ARES videos

### Fire Detection using FIRMS
- detect for fires using Mid-Wave Infrared (MWIR) and Long-Wave Infrared (LWIR) bands
- Other bands are used for masking. rejection of false positives, etc 

### Typical Temperature Ranges
- Surface of the Earth: ~300K
- Smoldering Fires: 600K to 800K
- Flaming Fires: ~1000K+

### Fire Detection Algorithm

FIRST STAGE:
- exclusion of invalid data 
- masking of known water and cloud pixels 

SECOND STAGE (tentative):
- identify potential fire pixels
- background characterization
- threshold tests (non-fire // unknown)

THIRD STAGE (REJECTION TESTING):
- sub glint rejection

HETEROGENEOUS LANDSCAPE REJECTION:
----------------------------------
// OVER LAND
- desert boundary rejection
- coast rejection
- forest cleaning rejection

// OVER WATER
- coast rejection
----------------------------------

OUTPUT: RASTER DATA IMAGE 
PIXEL SIZE is determined by the spatial resolution of the instrument onboard of the satellite

https://firms.modaps.eosdis.nasa.gov/map/#m:advanced;d:2025-06-29..2025-07-17,2025-07-17;l:fires_landsat_landsat,fires_modis_aqua,fires_modis_terra,fires_viirs_noaa20,fires_viirs_noaa21,fires_viirs_snpp,Suomi_NPP_Orbit_Asc,Suomi_NPP_Orbit_Dsc,firms_grids,firms_grids_label,country-outline,graticule,noaa20_snow,hlsl30-false-color,hlss30-true-color,noaa20_crtc,earth;@-93.1,36.6,4.9z

Pixel Elongation

Size of a pixel varies according to the spatial resolution of the sesnor onboard of the satellite 

### Data Latency
- delay between the observation and access to the data 
- wildfire events can be highly dynamic and vary rapidly over time

### Latency Terminology and Ranges
- URT (Ultra Real-Time): < 5min
- RT (Real-Time): 5min to 1hr
- NRT (Near Real-Time): 1hr to 3hrs
- Low Latency: 3hrs to 24hrs
- Expediated: 1 - 4 days 
- Standard Routine: 8 - 40 hrs <-- this is incredibly slow and should be a cause of concern

Satellite Observation -> Direct Broadcast -> SSEC Processing -> L2 URT Active Fire Processing 

Network of MODIS // VIIRS X-band ground stations network

### Landsat 8 / 9 
30m active fire processing data is posted within 30min
EROS processing center 
L2 Landsat Active Fire Detection / Processing

16 day orbit cycle / 8 day out of phase between the two satellites

### Real-Time Data 
GEOS-18 / GOES-19
10-15min latency

### Park Burn
Tends to occur in the afternoon and evening hours (18:00) for diurnal (daily) cycle

diurnal means daily cycle

### Atmospheric Factors impacting fire monitoring
- cloud cover
- smoke
- fog

### Biophysical Setting // Factors 
- forest canopy
- less forested areas
- terrain

Example: collision of cumulusj and pyrocumulus clouds effects a satellite's ability to detect fires

How can smoke from wildfires be detected during cloudly times?
NOAA 20 and NOAA 21 aerosol indices can be used to detect smoke plume. This data is coarse, so it might be difficult ot get the data during cloudy times

### RADAR Data 
- it has been used for mapping burned areas for cloudy areas within higher latitudes 
- ISAR mission (L-band SAR) to measure burned areas to find hazardour areas 

### Geostationary Data 
- be cautious when it is within use (only shows pixels with high amounts of confidence)