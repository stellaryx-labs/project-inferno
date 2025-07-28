Docs to save the config: https://docs.kepler.gl/docs/keplergl-jupyter#config

### 0x01 \> Fire Severity Classification (Palisades / Eaton Fire)
\- Use attributes such as Brightness, Brightness temperature 21/31 (Kelvin), FRP, Confidence, and Type to classify fire severity (low, medium, high)
\- Train machine learning models on these features for severity prediction
\- Provide confidence scores for each prediction
\- **Helpful datasets:** MODIS/VIIRS fire detection datasets, NASA FIRMS, local fire incident reports, sensor calibration datasets

simple fire severity over time using MODIS/VIIRS data

### 0x02 \> Thermal Signature Fingerprinting (Palisades / Eaton Fire)
\- Capture and store unique thermal patterns using Brightness, Brightness temperature 21/31, and FRP
\- Compare real-time sensor data (including Scan, Track, DayNight) to known fire signatures for identification
\- Support for multiple sensor types (infrared, thermal cameras) reflected in the data
\- **Helpful datasets:** MODIS/VIIRS thermal anomaly datasets, infrared camera data archives, historical fire event thermal profiles

fingerprinting and show graphs of the fire signature (polygon over map)

### 0x03 \> Most Dangerous Fires (Palisades / Eaton Fire)
\- Rank hotspots using severity (Brightness, FRP, Confidence), spread rate (Scan, Track), and proximity to critical assets (Latitude, Longitude)
\- Use Type and DayNight to further refine danger assessment
\- **Helpful datasets:** MODIS/VIIRS fire/hotspot datasets, critical asset geospatial datasets, local infrastructure maps, weather data

// plot points on the map with the most amount of damage, severity, and spread rate (economic toil)

### 0x04 \> Predictive Fire Spread Estimator (Palisades / Eaton Fire)
\- Model fire spread using Latitude, Longitude, Scan, Track, Acq_Date, Acq_Time, and weather/terrain/fuel data
\- Visualize predicted fire paths using mapped coordinates and time attributes
\- **Helpful datasets:** MODIS/VIIRS fire progression datasets, meteorological data (wind, humidity, temperature), terrain elevation models, vegetation/fuel maps

use the above datasets for plotting the tracks of estimated fire spread over time