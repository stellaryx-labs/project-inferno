"""
Main function to display the contents of the severity page within the Streamlit application

Visuals include the following:
>> HDF images before masking
>> Masks
>> Cleaned HDF images (after masking)
>> NBR heat map
>> dNBR linear map
>> RdNBR linear map
"""

import streamlit as st
import os

# Functions for rendering images and HTML visualizations
def _display_image(image_path, height=400, width=900):
    complete_image_path = os.path.join(
        "./captures",
        image_path)
    st.image(complete_image_path, use_container_width=False, width=width)

# Archived, but keeping for reference for anyone who wants to do a live rendering of plotly charts
def _display_html_visualization(filename, height=400, width=900):
    html_path = os.path.join(
        "./data_processing/streamlit_visualizations",
        filename)
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            st.components.v1.html(html_content, height=height, width=width)
    else:
        st.warning(f"Visualization '{filename}' not found.")

# Stylistic functions for rendering Markdown content
def _render_subtitle(subtitle):
    st.markdown(
        f"<h2 style='font-size:1.5em;'>{subtitle}</h2>",
        unsafe_allow_html=True)

def display_severity():
    st.text("Note: This page may take a minute to load...please be patient")

    _render_subtitle("NBR Bands")
    _display_image("nbr_visualizations.png")

    _render_subtitle("dNBR over Time (MOD)")
    _display_image("dnbr_over_time_mod.png")

    _render_subtitle("RdNBR over Time (MOD)")
    _display_image("rdnbr_over_time_mod.png")

    st.markdown("""
        <h4>All Interactive Visualizations in <b>captures</b></h4>
          <ul>
            <li><code>data_processing/visualizations/nbr_visualization.html</code>: NBR Visualizations</li>
            <li><code>data_processing/visualizations/dnbr_mod_over_time.html</code>: dNBR over time (MODIS)</li>
            <li><code>data_processing/visualizations/dnbr_myd_over_time.html</code>: dNBR over time (MYD09A1)</li>
            <li><code>data_processing/visualizations/rdnbr_mod_over_time.html</code>: RdNBR over time (MODIS)</li>
            <li><code>data_processing/visualizations/rdnbr_myd_over_time.html</code>: RdNBR over time (MYD09A1)</li>
          </ul>
        <h4>All Static Visualizations in <b>captures</b></h4>
          <ul>
            <li><code>captures/nbr_visualizations.png</code>: NBR Visualizations</li>
            <li><code>captures/dnbr_over_time_mod.png</code>: dNBR over time (MODIS)</li>
            <li><code>captures/dnbr_over_time_myd.png</code>: dNBR over time (MYD09A1)</li>
            <li><code>captures/rdnbr_over_time_mod.png</code>: RdNBR over time (MODIS)</li>
            <li><code>captures/rdnbr_over_time_myd.png</code>: RdNBR over time (MYD09A1)</li>
          </ul>
    """, unsafe_allow_html=True)
