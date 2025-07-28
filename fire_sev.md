https://burnseverity.cr.usgs.gov/glossary#dnbr

## TODO
- download the band composites for MODIS of the fire on a specific date and show the NBR visually
- why is it normalized? how does the math behidn normalization work?

- fire severity over time according to the defs of NDBI
- write a 5min section within the article explaining this section of the project
- https://burnseverity.cr.usgs.gov/products/mtbs (make a sequence imagery of this)
- make a sevrity chart over time 
- make calculations and reasoning for which sensor data to use 
- outline data source retrieval and processing using numpy and pandas

# Fire Severity Analysis
Aggregate severity scores by date/time.
Plot severity over time (e.g., line chart: x-axis = time, y-axis = severity)

## Data Derivation 

Downloading Granules 
Granules are the individual data files that make up a dataset. They can be downloaded from various sources, including NASA's Earthdata Search, LP DAAC, and other data repositories.

Paper Ref: https://essd.copernicus.org/articles/13/1925/2021/essd-13-1925-2021.pdf

> MODIS/Terra Surface Reflectance 8-Day L3 Global 500m SIN Grid V061 (MOD09A1):
> https://search.earthdata.nasa.gov/search/granules?p=C2343111356-LPCLOUD!C2343111356-LPCLOUD&pg[1][v]=t&pg[1][gsk]=-start_date&q=MOD09A1&fi=MODIS&fdc=Land%2BProcess%2BDistributed%2BActive%2BArchive%2BCenter%2B%2528LPDAAC%2529&tl=1352288806.226!5!!&lat=24.936748217822768&long=-51.81333726997593

> MODIS/Aqua Surface Reflectance 8-Day L3 Global 500m SIN Grid V061 (MYD09A1)
> MODIS/Terra+Aqua Burned Area Monthly L3 Global 500m SIN Grid V061 (MCD64A1)

"""
The MOSEV database was built using the following remote
sensing data available since November 2000 as input (Fig. 1).
– All scenes of MODIS Terra MOD09A1 and Aqua
MYD09A1 version 6. Terra MOD09A1 and Aqua
MYD09A1 scenes are 8 d composites with seven surface reflectance bands and quality information at a spatial resolution of 500 m and global coverage. The reflectance value of each pixel is the best possible observation in the 8 d period, selected according to quality criteria including cloud cover, cloud shadow, solar
zenith and aerosol loading.
– All scenes of MCD64A1 version 6 product. MCD64A1
is a monthly 500 m pixel product that contains daily
global information on burn date, uncertainty in burn
date, quality assurance indicators, and first and last day
of the year of reliable change detection.
MOD09A1, MYD09A1 and MCD64A1 data were downloaded from the Land Processes Distributed Active Archive
Center (LP-DAAC): https://lpdaac.usgs.gov/ (last access: 1
November 2020).
"""


# Plotting the Satellite Fleet 
-> Aqua // Terra: MODIS
-> Suomi NPP // NOAA-20 // NOAA-21: VIIRS

## Sensor Information
-> MODIS        // [ firms_data/MODIS_C61.csv ]       -> legacy wide-area fire detection (1km/500m resolution)
-> VIIRS J1     // [ firms_data/J1_VIIRS_C2.csv ]     -> 375m high-res thermal fire detection (NOAA-20)
-> VIIRS J2     // [ firms_data/J2_VIIRS_C2.csv ]     -> 375m high-res thermal fire detection (NOAA-21)
-> VIIRS Suomi  // [ firms_data/SUOMI_VIIRS_C2.csv ]  -> 375m fire detection from Suomi NPP satellite
-> LANDSAT      // [ firms_data/LANDSAT.csv ]         -> 30m resolution for detailed post-burn and land change analysis

### Instrument
- Moderate Resolution Imaging Spectroradiometer (MODIS) aboard the Aqua and Terra satellites
- Visible Infrared Imaging Radiometer Suite (VIIRS) aboard S-NPP, NOAA 20 and NOAA 2

### Spectral Band and Characteristics of the Instruments
**MODIS**: 
- Spatial: 250 m, 500 m, 1000 m
- Spectral: 36 spectral bands ranging in wavelength from 0.4 µm to 14.4 µm
- Temporal: 1-2 days
- Source: https://www.earthdata.nasa.gov/data/instruments/modis

**VIIRS**:
- Spatial: 375 m, 750 m
- Spectral: 22 spectral bands ranging in wavelength from 0.402 µm to 12.49 µm
- Temporal: Daily
- Source: https://www.earthdata.nasa.gov/data/instruments/viirs

### Spectral Bands

#### MODIS Spectral Bands
Source: https://www.earthdata.nasa.gov/data/instruments/modis/spectral-bands
- Band 1: 620–670nm (Shortwave/VIS)
- Band 2: 841–876nm (Shortwave/NIR)
- Band 3: 459–479nm (Shortwave/VIS)
- Band 4: 545–565nm (Shortwave/VIS)
- Band 5: 1230–1250nm (Shortwave/NIR)
- Band 6: 1628–1652nm (Shortwave Infrared/SWIR)
- Band 7: 2105–2155nm (Shortwave Infrared/SWIR)
- Band 8: 405–420nm (Shortwave/VIS)
- Band 9: 438–448nm (Shortwave/VIS)
- Band 10: 483–493nm (Shortwave/VIS)
- Band 11: 526–536nm (Shortwave/VIS)
- Band 12: 546–556nm (Shortwave/VIS)
- Band 13h: 662–672nm (Shortwave/VIS)
- Band 13l: 662–672nm (Shortwave/VIS)
- Band 14h: 673–683nm (Shortwave/VIS)
- Band 14l: 673–683nm (Shortwave/VIS)
- Band 15: 743–753nm (Shortwave/VIS)
- Band 16: 862–877nm (Shortwave/NIR)
- Band 17: 890–920nm (Shortwave/NIR)
- Band 18: 931–941nm (Shortwave/NIR)
- Band 19: 915–965nm (Shortwave/NIR)
- Band 20: 3.660–3.840µm (Longwave thermal Infrared/TIR)
- Band 21: 3.929–3.989µm (Longwave thermal Infrared/TIR) <--- Brightness // MODIS
- Band 22: 3.929–3.989µm (Longwave thermal Infrared/TIR) <--- Brightness // MODIS
- Band 23: 4.020–4.080µm (Longwave thermal Infrared/TIR)
- Band 24: 4.433–4.498µm (Longwave thermal Infrared/TIR)
- Band 25: 4.482–4.549µm (Longwave thermal Infrared/TIR)
- Band 26: 1360–1390nm (Shortwave/NIR)
- Band 27: 6.535–6.895µm (Longwave thermal Infrared/TIR)
- Band 28: 7.175–7.475µm (Longwave thermal Infrared/TIR)
- Band 29: 8.400–8.700µm (Longwave thermal Infrared/TIR)
- Band 30: 9.580–9.880µm (Longwave thermal Infrared/TIR)
- Band 31: 10.780–11.280µm (Longwave thermal Infrared/TIR) <--- Bright_T31 // MODIS
- Band 32: 11.770–12.270µm (Longwave thermal Infrared/TIR)
- Band 33: 13.185–13.485µm (Longwave thermal Infrared/TIR)
- Band 34: 13.485–13.785µm (Longwave thermal Infrared/TIR)
- Band 35: 13.785–14.085µm (Longwave thermal Infrared/TIR)
- Band 36: 14.085–14.385µm (Longwave thermal Infrared/TIR)

### VIIRS Spectral Bands
Source: https://www.earthdata.nasa.gov/data/instruments/viirs/spectral-bands

The VIIRS instruments acquire data in two native spatial resolutions:
Bands I1-5: 375m
Bands M1-16: 750m

- Band I1: 0.6–0.68µm (Visible/Reflective)
- Band I2: 0.85–0.88µm (Near Infrared)
- Band I3: 1.58–1.64µm (Shortwave Infrared)
- Band I4: 3.55–3.93µm (Medium-wave Infrared) <--- Brightness // VIIRS
- Band I5: 10.5–12.4µm (Longwave Infrared) 
- Band M1: 0.402–0.422µm (Visible/Reflective)
- Band M2: 0.436–0.454µm (Visible/Reflective)
- Band M3: 0.478–0.488µm (Visible/Reflective)
- Band M4: 0.545–0.565µm (Visible/Reflective)
- Band M5: 0.662–0.682µm (Near Infrared)
- Band M6: 0.739–0.754µm (Near Infrared)
- Band M7: 0.846–0.885µm (Shortwave Infrared)
- Band M8: 1.23–1.25µm (Shortwave Infrared)
- Band M9: 1.371–1.386µm (Shortwave Infrared)
- Band M10: 1.58–1.64µm (Shortwave Infrared)
- Band M11: 2.23–2.28µm (Medium-wave Infrared)
- Band M12: 3.61–3.79µm (Medium-wave Infrared)
- Band M13: 3.97–4.13µm (Longwave Infrared)
- Band M14: 8.4–8.7µm (Longwave Infrared)
- Band M15: 10.26–11.26µm (Longwave Infrared)
- Band M16: 11.54–12.49µm (Day/Night)
- Band DNB: 0.5–0.9µm (Visible/Reflective)

### Relevant Spectral Bands Included within the Dataset
https://www.earthdata.nasa.gov/data/tools/firms/active-fire-data-attributes-modis-viirs
- Band 21: 3.929–3.989µm (Longwave thermal Infrared/TIR) <--- Brightness // MODIS
- Band 22: 3.929–3.989µm (Longwave thermal Infrared/TIR) <--- Brightness // MODIS
- Band 31: 10.780–11.280µm (Longwave thermal Infrared/TIR) <--- Bright_T31 // MODIS
- Band I4: 3.55–3.93µm (Medium-wave Infrared) <--- Brightness // VIIRS
- Band I5: 10.5–12.4µm (Longwave Infrared) <--- Bright_ti5 // VIIRS

### Calculatable Products
- Normalized Burn Ratio (NBR)... NBR = (NIR - SWIR) ÷ (NIR + SWIR)
- Relativized differenced Normalized Burn Ratio (RdNBR)... RdNBR = dNBR / SquareRoot(ABS(NBR pre-fire / 1000))
- dNBR (difference between pre-fire and post-fire NBR)... dNBR = NBR pre-fire – NBR post-fire

- **Output**: 6 Class Thematic Burn Severity Classification (derived from NBR) (NBR6)
6 Class Thematic Burn Severity Classification (derived from NBR) (NBR6) – A continuous NBR image thresholded to yield thematic burn severity classes, including unburned to low, low, moderate, high, increased greenness and non-processing mask/area.
- 0x00 > Unburned
- 0x01 > Low
- 0x02 > Moderate
- 0x03 > High
- 0x04 > Increased Greenness
- 0x05 > Non-Processing Mask/Area


### How is Burn Severity Displayed?
NBR, dNBR and RdNBR data

### Data Preparation
- MOSEV: A global burn severity database from MODIS (2000-2020) [https://zenodo.org/records/4265209]
- Detemining which sensor I should use for the analysis: MODIS or VIIRS

### NBR Band Specifications:
MODIS (Terra & Aqua)

NIR Band: Band 2 (841–876 nm) at 250 m resolution (for the Terra and Aqua MOD09/MYD09 products)

SWIR2 Band: Band 7 (2105–2155 nm) at 500 m resolution (for the Terra and Aqua MOD09/MYD09 products)

Resolution Challenge: MODIS provides the NIR band at 250 m, but the SWIR2 band is at a coarser 500 m resolution, which can lead to spatial mismatch for detailed assessments of burn severity.

VIIRS (NOAA-20 and Suomi NPP)

NIR Band: Band M7 (841–875 nm) at 375 m resolution

SWIR2 Band: Band M11 (2110–2170 nm) at 375 m resolution

### Steps

- Step 0x00 > Calculate the "Severity"
   - understand the data and choose which sensor data to rely on
   - each step of the graph will be 12hr intervals (change as needed for finer granularity)
   - use the data to calculate the severity of the fire
   - detemine which sensor data should be used
   - facet the dataset using the polygon of the fire over the specific time period
   - plot the severity of the fire over time

- Step 0x01 > Get the data
  - Data Format... X: Time, Y: Severity
  - Give the plot relevant labels + title
- Step 0x02 > Plot the data
  - Use a line chart to plot the severity of the fire over time
  - Use the following libraries:
    - Seaborn

### Data Fields
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

Option 0x00 >
Calculate NBR and NDVI from satellite imagery (using NIR, SWIR, and Red bands).
Compute dNBR (difference between pre-fire and post-fire NBR).
Optionally, calculate RdNBR for normalization.
Threshold the dNBR or RdNBR values to assign burn severity classes (e.g., unburned, low, moderate, high).
Train a machine learning model (e.g., Random Forest, SVM) using these indices and labeled data if available.