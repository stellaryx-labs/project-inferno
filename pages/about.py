def display_about():
    import streamlit as st

    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Russo+One&display=swap');
        h2, h4 {
            font-family: 'Russo One', monospace !important;
            font-weight: 500 !important;
            letter-spacing: 1.5px;
            color: #ff6600;
        }
        .description {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <p class="description" style="color: white;">
        This project aims to leverage open-source Earth Observation (EO) data to provide autonomous geospatial analytics for wildfire intelligence.
        The case study focuses on the Eaton and Palisades fires in California in 2025, utilizing advanced remote sensing techniques to analyze fire severity and impact.
        </p>

        <h4>Key Features:</h4>
        <ul class="description">
            <li>Fire mapping using NASA satellite remote sensing data</li>
            <li>Severity analysis through algorithms to calculate NBR, dNBR, and RdNBR</li>
            <li>Visualizations of fire dynamics</li>
        </ul>

        <h4>Technologies Used:</h4>
        <ul class="description">
            <li><b>Python</b> for data processing and analysis</li>
            <li><b>Streamlit</b> for interactive web applications</li>
            <li><b>GDAL</b> and Rasterio for geospatial data handling</li>
            <li><b>Geopandas</b> for spatial data manipulation</li>
        </ul>

        <h4>Data Sources:</h4>
        <ul class="description">
            <li><a href="https://firms.modaps.eosdis.nasa.gov/usfs/map/">NASA FIRMS</a> for fire mapping data</li>
            <li><a href="https://search.earthdata.nasa.gov/">NASA EarthData Search</a> for HDF files</li>
        </ul>

        <div>
          <h4>Data from Sensor Configurations</h4>
          <ul>
            <li>MODIS: <code>firms_data/MODIS_C61.csv</code> &mdash; Wide-area fire detection (1km/500m)</li>
            <li>VIIRS J1: <code>firms_data/J1_VIIRS_C2.csv</code> &mdash; 375m, NOAA-20</li>
            <li>VIIRS J2: <code>firms_data/J2_VIIRS_C2.csv</code> &mdash; 375m, NOAA-21</li>
            <li>VIIRS Suomi: <code>firms_data/SUOMI_VIIRS_C2.csv</code> &mdash; 375m, Suomi NPP</li>
            <li>LANDSAT: <code>firms_data/LANDSAT.csv</code> &mdash; 30m, post-burn analysis</li>
          </ul>
          <h4>HDF Files</h4>
          <ul>
            <li>MCD64A1A: Burned Area Monthly L3 Global 500m</li>
            <li>MOD09A1: Terra Vegetation Indices 16-Day L3 Global 500m</li>
            <li>MYD09A1: Aqua Vegetation Indices 16-Day L3 Global 500m</li>
          </ul>
          <h4>Visualizations</h4>
          <ul>
            <li><code>data_processing/visualizations/dnbr_visualization.html</code>: dNBR fire severity</li>
            <li><code>data_processing/visualizations/RdNBR_mod_over_time.html</code>: RdNBR over time (MODIS)</li>
            <li><code>data_processing/visualizations/RdNBR_myd_over_time.html</code>: RdNBR over time (MYD09A1)</li>
            <li><code>data_processing/visualizations/dnbr_mod_over_time.html</code>: dNBR over time (MODIS)</li>
            <li><code>data_processing/visualizations/dnbr_myd_over_time.html</code>: dNBR over time (MYD09A1)</li>
            <li><code>data_processing/visualizations/dnbr_aggregated.html</code>: Aggregated dNBR</li>
          </ul>
          <h4>Cleaned Bands</h4>
          <ul>
            <li>MODIS: <code>data_processing/MOD09A1/cleaned_bands/</code></li>
            <li>MYD09A1: <code>data_processing/MYD09A1/cleaned_bands/</code></li>
          </ul>
        </div>
    """, unsafe_allow_html=True)
