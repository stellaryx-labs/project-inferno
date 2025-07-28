Docs to save the config: https://docs.kepler.gl/docs/keplergl-jupyter#config

### 0x01 \> Fire Severity Classification (Palisades / Eaton Fire) [Severity Analysis 🔥]
\- Use attributes such as Brightness, Brightness temperature 21/31 (Kelvin), FRP, Confidence, and Type to classify fire severity (low, medium, high)
\- Train machine learning models on these features for severity prediction
\- Provide confidence scores for each prediction
\- **Helpful datasets:** MODIS/VIIRS fire detection datasets, NASA FIRMS, local fire incident reports, sensor calibration datasets

simple fire severity over time using MODIS/VIIRS data

### 0x03 \> Most Dangerous Fires (Palisades / Eaton Fire) [Danger Assessment 🛑]
\- Rank hotspots using severity (Brightness, FRP, Confidence), spread rate (Scan, Track), and proximity to critical assets (Latitude, Longitude)
\- Use Type and DayNight to further refine danger assessment
\- **Helpful datasets:** MODIS/VIIRS fire/hotspot datasets, critical asset geospatial datasets, local infrastructure maps, weather data

// plot points on the map with the most amount of damage, severity, and spread rate (economic toil)
- danger report // total economic damage, spread rate, and severity

### 0x04 \> Predictive Fire Spread Estimator (Palisades / Eaton Fire) [Fire Spread Prediction 🚒]
\- Model fire spread using Latitude, Longitude, Scan, Track, Acq_Date, Acq_Time, and weather/terrain/fuel data
\- Visualize predicted fire paths using mapped coordinates and time attributes
\- **Helpful datasets:** MODIS/VIIRS fire progression datasets, meteorological data (wind, humidity, temperature), terrain elevation models, vegetation/fuel maps

use the above datasets for plotting the tracks of estimated fire spread over time