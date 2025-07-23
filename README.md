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

# To 
https://firms.modaps.eosdis.nasa.gov/academy
- [x] Data Ingestion and Manipulation
- [ ] Using FIRMS API
- [ ] Data Visualization
- [ ] Data Subsetting
- finish the video tutorials on how to use the FIRMS website 