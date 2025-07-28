import streamlit as st

# Obtain MODIS data for the severity analysis
# Source for the data can be found at: https://firms.modaps.eosdis.nasa.gov/download/
def _obtain_severity_data():
    pass

"""
- Normalized Burn Ratio (NBR)... NBR = (NIR - SWIR) ÷ (NIR + SWIR)
- Relativized differenced Normalized Burn Ratio (RdNBR)... RdNBR = dNBR / SquareRoot(ABS(NBR pre-fire / 1000))
- dNBR (difference between pre-fire and post-fire NBR)... dNBR = NBR pre-fire – NBR post-fire
"""
# Calculate: Normalized Burn Ratio (NBR)... NBR = (NIR - SWIR) ÷ (NIR + SWIR)
def _calculate_nbr():
    pass

# Calculate: Relativized differenced Normalized Burn Ratio (RdNBR)... RdNBR = dNBR / SquareRoot(ABS(NBR pre-fire / 1000))
def _calculate_rdnbr():
    pass

# Calculate: Differenced Normalized Burn Ratio (dNBR)... dNBR = NBR pre-fire – NBR post-fire
def _calculate_dnbr():
    pass

"""
Main function to display the contents of the severity page within the Streamlit application
"""
def display_maps():
    pass

def display_chart():
    pass

def display_severity():
    st.markdown("# Severity Analysis 🔥")
    st.markdown("## WIP")