"""
EXTRACT THE FOLLOWING VALUES FROM THE MCD64A1 HDF4 FILE:
MCD64A1 burn day = Burn Date
MCD64A1 uncertainty in days = Burn Date Uncertainty

Obtained info about relevant attributes using the following command:
$ hdp dumpsds -h MCD64A1.A2025001.h08v05.061.2025070160807.hdf | grep -i Date  > mcd_date_fieldz.txt

LONG NAME ATTRIBUTES (containing the word "Date"):
- ordinal day of burn
- uncertainty in day of burn

Get documentation for the MCD64A1 product here:
https://lpdaac.usgs.gov/documents/101/MCD64A1_User_Guide_V6.pdf

Data Layer:
Burn Date, Burn Date Uncertainty, QA, First Day, and Last Day

* Burn Date: Ordinal day of burn (1-366) for each 500-m grid cell, with 0 = unburned land, -1 = unmapped
due to insufficient data, and -2 = water.

* Burn Date Uncertainty: Estimated uncertainty in date of burn, in days. Unburned and unmapped grid
cells will always have a value of 0 in this layer.

OUTPUT:
GeoTIFF (.tif) files with raster shape (2400×2400)

2400×2400 is the resolution of the MCD64A1 product, which is 500m per pixel.
500m is the resolution of the MCD64A1 product, which is 500m per pixel.
"""

# STEP 0x00 > LOAD HDF4 FILE and CREATE TIF OUTPUT CONTAINING DATE AND
# UNCERTAINTY DATA
from pyhdf.SD import SD, SDC
from osgeo import gdal
import os

hdf_file = os.path.abspath(
    "./data_processing/MCD64A1/MCD64A1.A2025001.h08v05.061.2025070160807.hdf")
reference_modis = os.path.abspath(
    "./data_processing/MOD09A1/MOD09A1.A2025001.h08v05.061.2025011011329.hdf")
output_burn = os.path.abspath("./data_processing/MCD64A1/MCD64A1_BurnDate.tif")
output_uncert = os.path.abspath(
    "./data_processing/MCD64A1/MCD64A1_BurnDateUncertainty.tif")

hdf = SD(hdf_file, SDC.READ)

# Function to find datasets by long_name attribute


def find_sds_by_longname(target_name):
    matches = {}
    for sds_name in hdf.datasets().keys():
        sds = hdf.select(sds_name)
        attrs = sds.attributes()

        long_name = attrs.get("long_name", "")

        if target_name.lower() in long_name.lower():
            matches[sds_name] = {
                "long_name": long_name,
                "data": sds[:],
                "attributes": attrs,
            }
    return matches

# Determine which file format to save it as


def save_geotiff(filename, array, ref_path, nodata_val=0):
    ref_ds = gdal.Open(ref_path)
    driver = gdal.GetDriverByName('GTiff')

    out_ds = driver.Create(
        filename,
        array.shape[1],
        array.shape[0],
        1,
        gdal.GDT_Int16
    )

    out_ds.SetGeoTransform(ref_ds.GetGeoTransform())
    out_ds.SetProjection(ref_ds.GetProjection())
    out_ds.GetRasterBand(1).WriteArray(array)
    out_ds.GetRasterBand(1).SetNoDataValue(nodata_val)
    out_ds.FlushCache()
    out_ds = None


# Extract both Burn Date and Uncertainty
burn_date_data = find_sds_by_longname("ordinal day of burn")
uncertainty_data = find_sds_by_longname("uncertainty in day of burn")


def print_dataset_info(label, entry, output_path):
    print(f"\n{'=' * 50}")
    print(f"{label} Dataset: [{entry['long_name']}]")
    print(f"  Output Path      : {output_path}")
    print(f"  Data Shape       : {entry['data'].shape}")
    print(f"  Sample Data      : {entry['data'][0, :10]}")
    print(f"{'=' * 50}\n")


# Print the data
for key, entry in burn_date_data.items():
    save_geotiff(output_burn, entry["data"], reference_modis)
    print_dataset_info("Burn Date", entry, output_burn)

for key, entry in uncertainty_data.items():
    save_geotiff(output_uncert, entry["data"], reference_modis)
    print_dataset_info("Burn Date Uncertainty", entry, output_uncert)
