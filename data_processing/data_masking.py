import os
import numpy as np
from osgeo import gdal
import re
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys

"""
 MODIS Land Surface Reflectance 500m State flags
 sur_refl_state_500m	UINT16	(see grid structure)

    Description:
	MODIS Land Surface Reflectance 500m State flags.

	Bit    Description
	15     PGE11 internal snow mask;
	       key: snow (1) or no snow (0)
	14     BRDF correction performed;
	       key: yes (1) or no (0)
	13     Pixel is adjacent to cloud;
	       key: yes (1) or no (0)
	12     Snow/ice flag;
	       key: yes (1) or no (0)
	11     PGE11 internal fire mask;
	       key: fire (1) or no fire (0)
	10     PGE11 internal cloud mask;
	       key: cloudy (1) or clear (0)
	8-9    Cirrus detected;
	       key: 00 (0): none
	            01 (1): small
		    10 (2): average
		    11 (3): high
	6-7    Aerosol quantity;
	       key: 00 (0): climatology
	            01 (1): low
		    10 (2): average
		    11 (3): high
	3-5    Land/water flag;
	       key: 000 (0): shallow ocean
        	    001 (1): land
	            010 (2): ocean coastlines and land shorelines
	            011 (3): shallow inland water
	            100 (4): ephemeral water
	            101 (5): deep inland water
	            110 (6): ocean
	            111 (7): surface unknown (treated as land)
	2      Cloud shadow;
	       key: yes (1) or no (0)
	0-1    Cloud state;
	       key: 00 (0): clear
	            01 (1): cloudy
        	    10 (2): mixed
	            11 (3): not set, assumed clear
"""


def print_section_header(title):
    print(f"\n{'=' * 60}\n{title}\n{'=' * 60}")


def print_subdatasets_info(hdf_ds):
    print_section_header("Subdatasets Information")
    subdatasets = hdf_ds.GetSubDatasets()
    print(f"Total subdatasets: {len(subdatasets)}")
    print("Available subdatasets:")
    for i, (name, _) in enumerate(subdatasets):
        print(f"  [{i}] {name}")


def print_band_info(band_idx, band_name, band_data, masked_data):
    print_section_header(f"Band {band_idx} - {band_name}")
    print(f"  Raw Data Shape     : {band_data.shape}")
    print(f"  Masked Data Shape  : {masked_data.shape}")
    print(f"  Raw Sample         : {band_data[0, :10]}")
    print(f"  Masked Sample      : {masked_data[0, :10]}")


def print_mask_stats(mask):
    print_section_header("Mask Statistics")
    print(f"  Valid pixels (mask==1): {np.sum(mask == 1)}")
    print(f"  Invalid pixels (mask==0): {np.sum(mask == 0)}")


def build_terrestrial_clear_mask(cf_array: np.ndarray) -> np.ndarray:
    internal_snow = (cf_array >> 15) & 1
    snow_ice_flag = (cf_array >> 12) & 1
    internal_cloud = (cf_array >> 10) & 1
    land_water_flag = (cf_array >> 3) & 0b111
    is_land = land_water_flag == 1
    clear = (internal_cloud == 0) & (internal_snow == 0) & (snow_ice_flag == 0)
    mask = is_land & clear
    return mask


mod_hdfs = [
    'MOD09A1.A2024361.h08v05.061.2025004043815.hdf',
    'MOD09A1.A2025001.h08v05.061.2025011011329.hdf',
    'MOD09A1.A2025009.h08v05.061.2025022121649.hdf',
    'MOD09A1.A2025017.h08v05.061.2025030194108.hdf',
    'MOD09A1.A2025025.h08v05.061.2025035205729.hdf'
]
myd_hdfs = [
    'MYD09A1.A2024361.h08v05.061.2025004044306.hdf',
    'MYD09A1.A2025001.h08v05.061.2025011010006.hdf',
    'MYD09A1.A2025009.h08v05.061.2025021213258.hdf',
    'MYD09A1.A2025017.h08v05.061.2025030194429.hdf',
    'MYD09A1.A2025025.h08v05.061.2025035182945.hdf'
]
mod_hdf_date_time = [{"start_date": "2024-12-26",
                      "start_time": "00:00:00.000000",
                      "end_date": "2025-01-02",
                      "end_time": "23:59:59.000000"},
                     {"start_date": "2025-01-01",
                      "start_time": "00:00:00.000000",
                      "end_date": "2025-01-08",
                      "end_time": "23:59:59.000000"},
                     {"start_date": "2025-01-09",
                      "start_time": "00:00:00.000000",
                      "end_date": "2025-01-16",
                      "end_time": "23:59:59.000000"},
                     {"start_date": "2025-01-17",
                      "start_time": "00:00:00.000000",
                      "end_date": "2025-01-24",
                      "end_time": "23:59:59.000000"},
                     {"start_date": "2025-01-25",
                      "start_time": "00:00:00.000000",
                      "end_date": "2025-02-01",
                      "end_time": "23:59:59.000000"}]
myd_hdfs_date_time = [{"start_date": "2024-12-26",
                       "start_time": "00:00:00.000000",
                       "end_date": "2025-01-02",
                       "end_time": "23:59:59.000000"},
                      {"start_date": "2025-01-01",
                       "start_time": "00:00:00.000000",
                       "end_date": "2025-01-08",
                       "end_time": "23:59:59.000000"},
                      {"start_date": "2025-01-09",
                       "start_time": "00:00:00.000000",
                       "end_date": "2025-01-16",
                       "end_time": "23:59:59.000000"},
                      {"start_date": "2025-01-17",
                       "start_time": "00:00:00.000000",
                       "end_date": "2025-01-24",
                       "end_time": "23:59:59.000000"},
                      {"start_date": "2025-01-25",
                       "start_time": "00:00:00.000000",
                       "end_date": "2025-02-01",
                       "end_time": "23:59:59.000000"}]

selected_bands = [
    "sur_refl_b01",
    "sur_refl_b02",
    "sur_refl_b03",
    "sur_refl_b04",
    "sur_refl_b05",
    "sur_refl_b06",
    "sur_refl_b07"]
cf_name = "sur_refl_state_500m"

selected_dataset_name = sys.argv[1] if len(sys.argv) > 1 else 'MOD09A1'
selected_hdf_index = int(sys.argv[2]) if len(sys.argv) > 2 else 0
selected_dataset = mod_hdfs if selected_dataset_name == 'MOD09A1' else myd_hdfs
name_hdf = selected_dataset[selected_hdf_index]
hdf_date_time = mod_hdf_date_time if selected_dataset_name == 'MOD09A1' else myd_hdfs_date_time
hfd_date_time = hdf_date_time[selected_hdf_index]
input_hdf = os.path.abspath(
    f'./data_processing/{selected_dataset_name}/' + name_hdf)
output_dir = os.path.abspath(
    f'./data_processing/{selected_dataset_name}/cleaned_bands/{name_hdf}/')
os.makedirs(output_dir, exist_ok=True)
sl_output_dir = os.path.abspath(
    f'./data_processing/{selected_dataset_name}/cleaned_bands/{name_hdf}/')
os.makedirs(sl_output_dir, exist_ok=True)

bands = []
band_date = None
cf_band = None

# 1. Open HDF file and list subdatasets
hdf_ds = gdal.Open(input_hdf)
if hdf_ds is None:
    raise RuntimeError("Failed to open HDF file")
print_subdatasets_info(hdf_ds)

# 2. Identify and select bands of interest
for i, (name, _) in enumerate(hdf_ds.GetSubDatasets()):
    match = re.match(r'(HDF4_EOS):([^:]+):"([^"]+)":([^:]+):(.+)', name)
    if match:
        subdataset_name = match.group(5)
        if subdataset_name in selected_bands:
            bands.append(name)
        elif subdataset_name == cf_name:
            cf_band = name
        elif subdataset_name == "sur_refl_day_of_year":
            band_date = name

# 3. Build the mask
print_section_header("cf Band Loading")
print(f"Loading cf band: {cf_band}")
cf_ds = gdal.Open(cf_band)
cf = cf_ds.GetRasterBand(1).AsMDArray().ReadAsArray()
print(f"cf band shape: {cf.shape}, dtype: {cf.dtype}")

print_section_header("Building Terrestrial Clear Mask")
mask = build_terrestrial_clear_mask(cf)
print_mask_stats(mask)

# 4. Load and save band date if available
if band_date:
    print_section_header("Band Date Extraction")
    print(f"Loading band date: {band_date}")
    date_ds = gdal.Open(band_date)
    if date_ds is not None:
        band_date_data = date_ds.GetRasterBand(1).AsMDArray().ReadAsArray()
        print(f"Band date shape: {band_date_data.shape}")
        date_output_path = os.path.join(output_dir, 'band_date.tif')
        driver = gdal.GetDriverByName('GTiff')
        out_ds = driver.Create(date_output_path,
                               date_ds.RasterXSize,
                               date_ds.RasterYSize,
                               1,
                               date_ds.GetRasterBand(1).DataType)
        out_ds.SetGeoTransform(date_ds.GetGeoTransform())
        out_ds.SetProjection(date_ds.GetProjection())
        out_ds.GetRasterBand(1).WriteArray(band_date_data)
        out_ds.GetRasterBand(1).SetNoDataValue(0)
        out_ds.FlushCache()
        out_ds = None
        date_ds = None
        print(f"Saved band date to {date_output_path}")

# 5. Apply mask to each band and save
for i, band_name in enumerate(bands, start=1):
    band_ds = gdal.Open(band_name)
    band_data = band_ds.GetRasterBand(1).AsMDArray().ReadAsArray()
    masked_data = np.where(mask == 1, band_data, 0)
    print_band_info(i, band_name, band_data, masked_data)
    output_path = os.path.join(output_dir, f'band{i}_masked.tif')
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(output_path,
                           band_ds.RasterXSize,
                           band_ds.RasterYSize,
                           1,
                           band_ds.GetRasterBand(1).DataType)
    out_ds.SetGeoTransform(band_ds.GetGeoTransform())
    out_ds.SetProjection(band_ds.GetProjection())
    out_ds.GetRasterBand(1).WriteArray(masked_data)
    out_ds.GetRasterBand(1).SetNoDataValue(0)
    out_ds.FlushCache()
    out_ds = None
    band_ds = None
    print(f"  Saved masked band {i} to {output_path}")

print_section_header("All Bands Processed and Saved")

# 6. Create visualizations of the masked bands
bit15 = (cf >> 15) & 1
bit12 = (cf >> 12) & 1
bit10 = (cf >> 10) & 1
land_water_flag = (cf >> 3) & 0b111

bands_raw = []
bands_masked = []
for band_name in bands:
    band_ds = gdal.Open(band_name)
    band_data = band_ds.GetRasterBand(1).AsMDArray().ReadAsArray()
    bands_raw.append(band_data)
    masked_data = np.where(mask == 1, band_data, 0)
    bands_masked.append(masked_data)
    band_ds = None

def build_heatmap(z, title, colorscale, row, col, fig, overlay_mask=None):
    if overlay_mask is not None:
        z = np.where(overlay_mask, z, np.nan)
    fig.add_trace(
        go.Heatmap(
            z=z,
            colorscale=colorscale,
            colorbar=dict(len=0.25, y=1 - (row - 1) * 0.33),
            zmin=np.nanmin(z),
            zmax=np.nanmax(z),
            showscale=(col == 7)
        ),
        row=row, col=col
    )
    fig.update_xaxes(showticklabels=False, row=row, col=col)
    fig.update_yaxes(showticklabels=False, row=row, col=col)
    annotations = list(fig.layout.annotations)
    annotations.append(dict(
        x=0.5,
        y=1.1,
        xref='paper',
        yref='paper',
        text=title,
        showarrow=False,
        font=dict(size=14)
    ))
    fig.layout.annotations = annotations


fig = make_subplots(
    rows=3, cols=7,
    subplot_titles=[
        "Bit 15 - Internal Snow", "Bit 12 - Snow/Ice Flag", "Bit 10 - Internal Cloud",
        "Bits 3-5 Land/Water Flag", "Final Terrestrial Clear Mask",
        "", ""] + [f"Raw Band {i + 1}" for i in range(7)] + [f"Masked Band {i + 1}" for i in range(7)],
    horizontal_spacing=0.01, vertical_spacing=0.05
)

cf_components = [bit15, bit12, bit10, land_water_flag, mask.astype(int)]
cf_colorscales = ['Reds', 'Reds', 'Reds', 'Greens', 'Greens']
for col, (arr, cs, title) in enumerate(
        zip(cf_components, cf_colorscales, fig.layout.annotations[:5]), 1):
    build_heatmap(arr, title.text, cs, row=1, col=col, fig=fig)
for col in range(6, 8):
    fig.update_xaxes(visible=False, row=1, col=col)
    fig.update_yaxes(visible=False, row=1, col=col)
for i, band in enumerate(bands_raw, 1):
    build_heatmap(band, f"Raw Band {i}", 'Viridis', row=2, col=i, fig=fig)
for i, band in enumerate(bands_masked, 1):
    build_heatmap(band, f"Masked Band {i}", 'Viridis', row=3, col=i, fig=fig)

fig.update_layout(
    height=1200,
    width=1800,
    title_text=f"{name_hdf} HDF Visualizations from " +
    hfd_date_time['start_date'] +
    " to " +
    hfd_date_time['end_date'],
    showlegend=False,
    margin=dict(
        t=80,
        b=40,
        l=40,
        r=40),
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(
        color='white'))

output_name = f"{output_dir}/modis_{name_hdf.lower()}_cf_and_bands.html"
fig.write_html(output_name)
streamlit_output_name = f"{sl_output_dir}/modis_{
    name_hdf.lower()}_cf_and_bands.html"
fig.update_layout(height=300, width=450)
fig.write_html(streamlit_output_name)
print_section_header("Visualization Saved")
print(f"  Visualization saved to: {output_name}")
print(f"  Streamlit visualization saved to: {streamlit_output_name}")
