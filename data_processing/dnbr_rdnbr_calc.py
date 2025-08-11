"""
MAKE SURE DATA IS MASKED USING THE FOLLOWING SCRIPT (refer to head -n 17 for `data_masking.py`):

CLI COMMAND TO CREATE FOR ALL THE HDF FILES {MOD09A1 which is (0 - 4)}:
$ for i in {0..4}; do python data_masking.py $i MOD09A1; done
$ for i in {0..4}; do python data_masking.py $i MYD09A1; done

RUNNING THE SCRIPT
$ python data_processing/dnbr_rdnbr_calc.py (MOD09A1 | MYD09A1)
"""

import os
import numpy as np
from osgeo import gdal
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# VISUALIZATION DIMENSIONS
VISUALIZATION_WIDTH = 1800
VISUALIZATION_HEIGHT = 1200

STREAMLIT_VISUALIZATION_WIDTH = 900
STREAMLIT_VISUALIZATION_HEIGHT = 600

# -- Procedure Overview --
# 1. Process all masked band data from the MOD09A1 and MYD09A1 directories
# 2. Load burn date and uncertainty data
# 3. Calculate NBR
# 4. Calculate dNBR
# 5. Calculate RdNBR
# 6. Visualize NBR, dNBR, and RdNBR for each of the masked bands
# 7. Finalize the figure layout and save the visualization as HTML
# 8. Save output data to file
# ------------------------

# 1. Process all HDF files in the MOD09A1 || MYD09A1 directories
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

burn_date_path = os.path.abspath(
    "./data_processing/visualizations/MCD64A1_BurnDate.tif")
burn_uncertainty_path = os.path.abspath(
    "./data_processing/visualizations/MCD64A1_BurnDateUncertainty.tif")
band_date = []

bands = {
    "MOD09A1": [
        {"name": "MOD09A1.A2024361.h08v05.061.2025004043815.hdf", "bands": [], "date": None, "nbr": None},
        {"name": "MOD09A1.A2025001.h08v05.061.2025011011329.hdf", "bands": [], "date": None, "nbr": None},
        {"name": "MOD09A1.A2025009.h08v05.061.2025022121649.hdf", "bands": [], "date": None, "nbr": None},
        {"name": "MOD09A1.A2025017.h08v05.061.2025030194108.hdf", "bands": [], "date": None, "nbr": None},
        {"name": "MOD09A1.A2025025.h08v05.061.2025035205729.hdf", "bands": [], "date": None, "nbr": None}
    ],
    "MYD09A1": [
        {"name": "MYD09A1.A2024361.h08v05.061.2025004044306.hdf", "bands": [], "date": None, "nbr": None},
        {"name": "MYD09A1.A2025001.h08v05.061.2025011010006.hdf", "bands": [], "date": None, "nbr": None},
        {"name": "MYD09A1.A2025009.h08v05.061.2025021213258.hdf", "bands": [], "date": None, "nbr": None},
        {"name": "MYD09A1.A2025017.h08v05.061.2025030194429.hdf", "bands": [], "date": None, "nbr": None},
        {"name": "MYD09A1.A2025025.h08v05.061.2025035182945.hdf", "bands": [], "date": None, "nbr": None}
    ]
}

# Path Structure:
# ./MOD09A1/cleaned_bands/MOD09A1.A2024361.h08v05.061.2025004043815.hdf/band6_masked.tif

def create_paths(hdfs):
    paths = []
    for hdf in hdfs:
        # Extract the name without the extension
        name_hdf = os.path.splitext(hdf)[0]
        for i in range(7):
            # Create the band name
            band_name = f"band{i + 1}_masked.tif"
            # Create the path for the masked bands
            path = os.path.abspath(
                f"./data_processing/{name_hdf.split('.')[0]}/cleaned_bands/{hdf}/{band_name}")
            paths.append(path)
    return paths


# Create paths for MOD09A1 and MYD09A1
mod_paths = create_paths(mod_hdfs)
myd_paths = create_paths(myd_hdfs)

# Print the paths for verification
print("MOD09A1 Paths:")
for path in mod_paths:
    print(path)
print("\nMYD09A1 Paths:")
for path in myd_paths:
    print(path)

# Confirm all the bands exist for both datasets (bands 1 - 7)
for path in mod_paths + myd_paths:
    print("Auditing: ", path)
    if not os.path.exists(path):
        print(f"[!] Path does not exist: {path}")
        # Specify the index of the path within mod_hdfs or myd_hdfs and the
        # command to run
        print(f"Please run the following command to create the missing band:\n")
        # Extract the type (MOD09A1 or MYD09A1)
        type_hdf = path.split('/')[-2].split('.')[0]
        hdf_index = mod_hdfs.index(path.split(
            '/')[-3] + ".hdf") if type_hdf == "MOD09A1" else myd_hdfs.index(path.split('/')[-3] + ".hdf")
        print(f"$ python data_masking.py {type_hdf} {hdf_index}")
        exit(1)

# Load the date band (band_date.tif) for each HDF file


def load_date_band(hdf_file):
    name_hdf = os.path.splitext(hdf_file)[0]
    date_band_path = os.path.abspath(
        f"./data_processing/{name_hdf.split('.')[0]}/cleaned_bands/{hdf_file}/band_date.tif")

    if not os.path.exists(date_band_path):
        raise FileNotFoundError(
            f"Date band file does not exist: {date_band_path}")

    print(f"Loading date band from: {date_band_path}")
    ds = gdal.Open(date_band_path)
    if ds is None:
        raise RuntimeError(f"Failed to open date band file: {date_band_path}")

    date_band = ds.GetRasterBand(1).ReadAsArray()
    if date_band is None:
        raise RuntimeError(
            f"Failed to read date band data from: {date_band_path}")

    return date_band

# Load the masked bands from the specified paths


def load_masked_bands(paths):
    for path in paths:
        print(f"Loading band from: {path}")
        ds = gdal.Open(path)
        if ds is None:
            raise RuntimeError(f"Failed to open band file: {path}")
        band = ds.GetRasterBand(1).ReadAsArray()
        if band is None:
            raise RuntimeError(f"Failed to read band data from: {path}")
        # Determine which dataset the band belongs to
        if "MOD09A1" in path:
            for entry in bands["MOD09A1"]:
                if entry["name"] in path:
                    entry["bands"].append(band)
                if entry["date"] is None:
                    entry["date"] = load_date_band(entry["name"])
                    print(f"Loaded date band for {entry['name']}")
        elif "MYD09A1" in path:
            for entry in bands["MYD09A1"]:
                if entry["name"] in path:
                    entry["bands"].append(band)
                if entry["date"] is None:
                    entry["date"] = load_date_band(entry["name"])
                    print(f"Loaded date band for {entry['name']}")
        else:
            raise ValueError(f"Unknown dataset type in path: {path}")
    return bands


# Load the masked bands for MOD09A1 and MYD09A1
bands_mod = load_masked_bands(mod_paths)
bands_myd = load_masked_bands(myd_paths)

# Check that all the HDFs have a "date" band loaded
for dataset, entries in bands_mod.items():
    print(f"\n{dataset} Bands:")
    for entry in entries:
        if entry["date"] is None:
            print(f"[!] No date band loaded for {entry['name']}")
        else:
            print(
                f"  {entry['name']} - Date band shape: {entry['date'].shape}")

# Print the shapes of the loaded bands for verification


def print_band_shapes(bands):
    for dataset, entries in bands.items():
        print(f"\n{dataset} Bands:")
        for entry in entries:
            print(f"  {entry['name']}:")
            for i, band in enumerate(entry["bands"]):
                print(f"    Band {i + 1} shape: {band.shape}")
            print(
                f"Date band shape: {
                    entry['date'].shape if entry['date'] is not None else 'N/A'}")


print_band_shapes(bands_mod)
print_band_shapes(bands_myd)

# 2. Load burn date and uncertainty data

# Load Date Data from MCD64A1
# MCD64A1_BurnDate.tif = Burn Date (ordinal day of burn)
# MCD64A1_BurnDateUncertainty.tif = Burn Date Uncertainty (in days)
# This is needed to determine the pre-fire and post-fire NBR dates


def load_burn_date_data(burn_date_path, burn_uncertainty_path):
    burn_date_ds = gdal.Open(burn_date_path)
    burn_uncertainty_ds = gdal.Open(burn_uncertainty_path)

    if burn_date_ds is None or burn_uncertainty_ds is None:
        raise RuntimeError("Failed to open burn date or uncertainty file")

    burn_date = burn_date_ds.GetRasterBand(1).ReadAsArray()
    burn_uncertainty = burn_uncertainty_ds.GetRasterBand(1).ReadAsArray()

    return burn_date, burn_uncertainty


burn_date, burn_uncertainty = load_burn_date_data(
    burn_date_path, burn_uncertainty_path)

# Print burn date and uncertainty data shapes
# They should be (2000x2000)
print("Burn date shape:", burn_date.shape)
print("Burn uncertainty shape:", burn_uncertainty.shape)

# 3. Calculate NBR
# Calculate the NBR (Normalized Burn Ratio) using the surface reflectance bands
"""
Normalized Burn Ratio (NBR) is calculated as:
NBR = [(NIR - SWIR) / (NIR + SWIR)] * 1000

NIR = p2 aka band 2  (sur_refl_b02) (841–876 nm)
SWIR = p7 aka band 7 (sur_refl_b07) (2105–2155 nm)

NBR = [ (p2 - p7) / (p2 + p7) ] * 1000
"""
# The following function calculates the NBR for two bands utilizing
# vectorized operations for efficiency


def calculate_nbr(band_2, band_7):
    # divide every single value in the band arrays by 10,000

    # Bands contained values for MODIS reflectance values
    # Convert to float and scale
    band_2_div = band_2.astype(np.float32) / 10000.0
    # Convert to float and scale
    band_7_div = band_7.astype(np.float32) / 10000.0

    # Print all values greatr than 1 in band_2 and band_7
    print("Values in band_2 greater than 1:", band_2_div[band_2_div > 1])
    print("Values in band_7 greater than 1:", band_7_div[band_7_div > 1])

    # Anamoly detected: there are values greater than 1 in the bands, which should not be the case
    #  1. Anisotropic Reflectance / BRDF Effects || 2. Cloud Contamination

    # X -> Clip to Valid Reflectance Range // this is lying as it keeps the data within the range, but it does not clearly define it as an outliner
    # USING A MASKING METHOD INSTEAD
    band_2_div_masked = np.where(
        (band_2_div > 1.0) | (
            band_2_div < 0.0),
        np.nan,
        band_2_div)
    band_7_div_masked = np.where(
        (band_7_div > 1.0) | (
            band_7_div < 0.0),
        np.nan,
        band_7_div)

    sum_ = band_2_div_masked + band_7_div_masked
    diff = band_2_div_masked - band_7_div_masked

    # Avoid divide-by-zero using np.where
    # Print out where division by zero occurs
    with np.errstate(divide='ignore', invalid='ignore'):
        nbr = np.where(sum_ == 0, 0, (diff / sum_))
    # Print the number of NaN values in the NBR array
    print("Number of NaN values in NBR array:", np.sum(np.isnan(nbr)))

    # Create a mask that converts values greater than 1 to NaN
    nbr = np.where(nbr > 1, np.nan, nbr)

    # Create a mask that converts values less than -1 to NaN
    nbr = np.where(nbr < -1, np.nan, nbr)

    return nbr

# MODIS reflectance values (e.g., in MYD09A1) are scaled by a factor of 10,000


def calc_nbr_for_bands_masked(bands_masked):
    # NIR band (sur_refl_b02)
    band_2 = bands_masked[1]

    # SWIR band (sur_refl_b07)
    band_7 = bands_masked[6]

    nbr = calculate_nbr(band_2, band_7)

    # Check if there are any NaN values in the NBR array
    if np.isnan(nbr).any():
        print("Warning: NBR contains NaN values. This may affect calculations.")

    # Print a sample of the NBR values
    print("Sample NBR values:", nbr.flatten()[:10])  # Print first 10 values

    # Print the number of values that are greater than 0 in the NBR array
    print("Number of NBR values greater than 0:", np.sum(nbr > 0))

    # Scale the NBR values by 1000 to match the MODIS reflectance scaling
    nbr = nbr * 1000.0  # Scale NBR values by 1000

    return nbr


# Calculating NBR for MOD09A1 and MYD09A1 masked bands
for dataset, entries in bands_mod.items():
    print(f"\n{dataset} Bands:")
    for entry in entries:
        entry_name = entry['name']
        print(f"  {entry_name}:", type(entry_name))
        nbr_for_dataset = calc_nbr_for_bands_masked(entry["bands"])
        # Save the NBR info to the bands dictionary
        bands["MOD09A1"][entries.index(entry)]["nbr"] = nbr_for_dataset
        print(nbr_for_dataset)

for dataset, entries in bands_myd.items():
    print(f"\n{dataset} Bands:")
    for entry in entries:
        entry_name = entry['name']
        print(f"  {entry_name}:", type(entry_name))
        nbr_for_dataset = calc_nbr_for_bands_masked(entry["bands"])
        # Save the NBR info to the bands dictionary
        bands["MYD09A1"][entries.index(entry)]["nbr"] = nbr_for_dataset
        print(nbr_for_dataset)

# Print for confirmation
print(bands["MYD09A1"][0]["nbr"])

# Print number of NBR values greater than 0 for bands["MYD09A1"][0]
print(
    "Number of NBR values greater than 1 for bands['MYD09A1'][0]:",
    np.sum(
        bands["MYD09A1"][0]["nbr"] > 1))

# Print sample of NBR values for bands["MYD09A1"][0] that are greater than 0
print("Sample NBR values greater than 1 for bands['MYD09A1'][0]:",
      bands["MYD09A1"][0]["nbr"][bands["MYD09A1"][0]["nbr"] > 1].flatten()[:10])

# Calculating dNBR for MOD09A1 and MYD09A1 masked bands
for dataset, entries in bands_mod.items():
    print(f"\n{dataset} Bands:")
    for entry in entries:
        print(f"  {entry['name']}:")
        for i, band in enumerate(entry["bands"]):
            print(f"    Band {i + 1} shape: {band.shape}")
            calc_nbr_for_bands_masked(band)

for dataset, entries in bands_myd.items():
    print(f"\n{dataset} Bands:")
    for entry in entries:
        print(f"  {entry['name']}:")
        for i, band in enumerate(entry["bands"]):
            print(f"    Band {i + 1} shape: {band.shape}")
            calc_nbr_for_bands_masked(band)

# Calculate the RdNBR (Relativized differenced Normalized Burn Ratio)

# 8. Calculate dNBR
# Before performing the calculation for the dNBR...
# Load Date Data from MCD64A1
# What do the MCD64A1 burn date values represent?
# The MCD64A1 burn date values represent the ordinal day of the year when
# a fire occurred.

"""
preNBR date < (MCD64A1 burn day − MCD64A1 uncertainty in days) -> preNBR_threshold
postNBR date > (MCD64A1 burn day + MCD64A1 uncertainty in days + 8 days) -> postNBR_threshold
MCD64A1 burn day values (per https://lpdaac.usgs.gov/documents/875/MCD64_User_Guide_V6.pdf):
0 = unburned land, -1 = unmapped
due to insufficient data, and -2 = water (exclude these from calculations).
"""
burn_date_data_mcd = load_burn_date_data(burn_date_path, burn_uncertainty_path)

# Print the burn date and uncertainty data
if burn_date_data_mcd is None or burn_uncertainty is None:
    print("Burn date or uncertainty data could not be loaded. Exiting.")

print("Burn date data shape:", burn_date.shape)
print("Burn uncertainty data shape:", burn_uncertainty.shape)

print(
    "Sample",
    "Burn date values:",
    burn_date.flatten()[
        :10])  # Print first 10 values
print(
    "Sample",
    "Burn uncertainty values:",
    burn_uncertainty.flatten()[
        :10])  # Print first 10 values

# Calculate preNBR and postNBR thresholds
# preNBR_threshold = burn_date - burn_uncertainty
# postNBR_threshold = burn_date + burn_uncertainty + 8

# if the date values are 0, -1, and -2... then the thresholds at that pixel should be set to -100
# 0 = unburned land, -1 = unmapped due to insufficient data, and -2 = water
preNBR_threshold = np.where(burn_date <= 0, -100, burn_date - burn_uncertainty)
postNBR_threshold = np.where(
    burn_date <= 0, -100, burn_date + burn_uncertainty + 8)

# Print the preNBR and postNBR thresholds
print(
    "Sample preNBR threshold values:",
    preNBR_threshold.flatten()[
        :10])  # Print first 10 values
print(
    "Sample postNBR threshold values:",
    postNBR_threshold.flatten()[
        :10])  # Print first 10 values

# Print the number of values that are greater than 0 in the preNBR and
# postNBR thresholds
print(
    "Number of preNBR threshold values greater than 0:",
    np.sum(
        preNBR_threshold > 0))
print(
    "Number of postNBR threshold values greater than 0:",
    np.sum(
        postNBR_threshold > 0))

# Find pixel positions where BOTH preNBR and postNBR thresholds are
# greater than 0
preNBR_mask = preNBR_threshold > 0
postNBR_mask = postNBR_threshold > 0

# Combine the masks to find pixels where both conditions are met
combined_mask_pre_post_nbr = preNBR_mask & postNBR_mask

# combined_mask_pre_post_nbr is a boolean array where True indicates both
# preNBR and postNBR thresholds are greater than 0

# Print the number of pixels where both preNBR and postNBR thresholds are
# greater than 0
pixels_nbr_date_masked = np.sum(combined_mask_pre_post_nbr)
print(
    f"Number of pixels with both preNBR and postNBR thresholds greater than 0: {pixels_nbr_date_masked}")

# Iterate through the boolean mask "combined_mask_pre_post_nbr" to find
# the preNBR and postNBR values
print(type(combined_mask_pre_post_nbr))  # Should be <class 'numpy.ndarray'>

# Find the earliest date (in this case any value greate than 32 and less
# than 361 [found via inspection of array contents using Pycharm debug
# mode])


def find_earliest_date(masked_dates):
    # Find the earliest date in the masked dates
    # Ignore values <= 32
    earliest_date = np.min(masked_dates[masked_dates > 32])
    return earliest_date

# Consolidate all masked dates from both MOD09A1 and MYD09A1 datasets


def consolidate_masked_dates(bands, dataset):
    masked_dates = []
    for entry in bands[dataset]:
        if entry["date"] is not None:
            date_band = entry["date"]
            # Apply the combined mask to the date band
            masked_date_band = date_band[combined_mask_pre_post_nbr]
            # Append the masked dates to the list
            masked_dates.append(masked_date_band)
        else:
            masked_dates.append(None)
    return masked_dates


masked_dates = consolidate_masked_dates(
    bands, "MOD09A1") + consolidate_masked_dates(bands, "MYD09A1")

# Find the earliest date across all masked dates
earliest = find_earliest_date(np.concatenate(masked_dates))
print(earliest)

# Format date band
# This is necessary because the format of the date band provided by NASA is super weird
# ie. 365 = 1st day of the year, 366 = 2nd day of the year, etc.

# OUTPUT: Efficiently find NBR values that fit within the preNBR condition (vectorized)
# you need to account for the fact the preNBR and postNBR thresholds contain -100
# this is a problem esp for preNBR condition values that are less than 0
# min date value is 361 this is because if we look at the dataset date range... the most late date is 2/1/2025 which is DOY of 32
# Earliest date is 361, which corresponds to (12/27) December 27th in
# non-leap years (like 2025)


def find_pre_nbr_vectorized(pre_nbr_threshold, dataset):
    dataset_data = bands[dataset]
    results = []
    for entry in dataset_data:
        if entry["date"] is not None:
            date_band = entry["date"]
            # we need to take into account values that are within the range of (361, 366) which are still less than the pre_nbr_threshold
            # pre_nbr_threshold starts at -100 (these are invalid pixels and the NBR should be NAN)
            # all the valid pixels are greater than 0. 1 = 1st day of the year, 2 = 2nd day of the year, etc. (this is also on the Julian calendar)
            # Broadcast pre_nbr_threshold to match date_band shape if needed
            # top value for date_band is 361 (this should also result the mask to be True)
            # to do this I added the following logic in conjunction with an or statement:
            # ((date_band > 360 and ((date_band - 366) < pre_nbr_threshold))

            # mask = ((date_band > 360 and ((date_band - 366) < pre_nbr_threshold)) or (date_band < pre_nbr_threshold)) & (pre_nbr_threshold > 0) // 7:32PM PST - AT
            # ('The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()',)

            # Vectorized logic: use np.logical_and and np.logical_or for
            # array-wise operations
            mask = (
                np.logical_or(
                    np.logical_and(
                        date_band > 360,
                        (date_band - 366) < pre_nbr_threshold),
                    date_band < pre_nbr_threshold) & (
                    pre_nbr_threshold > 0))

            results.append(mask)
        else:
            results.append(None)
    return results


def find_post_nbr_vectorized(post_nbr_threshold, dataset):
    dataset_data = bands[dataset]
    results = []
    for entry in dataset_data:
        if entry["date"] is not None:
            date_band = entry["date"]
            # Broadcast post_nbr_threshold to match date_band shape if needed
            mask = (date_band > post_nbr_threshold) & (post_nbr_threshold > 0)
            results.append(mask)
        else:
            results.append(None)
    return results


# Vectorized loop over all pixels where both preNBR and postNBR thresholds are valid
# Instead of looping pixel-by-pixel, process the entire mask at once
pre_nbr_masks_mod = find_pre_nbr_vectorized(preNBR_threshold, "MOD09A1")
pre_nbr_masks_myd = find_pre_nbr_vectorized(preNBR_threshold, "MYD09A1")

# Print the shapes of the preNBR masks
nt1, nt2, nt3, nt4, nt5 = np.sum(
    pre_nbr_masks_mod[0]), np.sum(
        pre_nbr_masks_mod[1]), np.sum(
            pre_nbr_masks_mod[2]), np.sum(
                pre_nbr_masks_mod[3]), np.sum(
                    pre_nbr_masks_mod[4])  # Count True values in the first MOD09A1 mask

# why does `nt5` have a smaller number of True values?

# Print: expression evaluation of the number of True values in each preNBR mask.. pixel of NBR date = date of which tje reflectance was taken
# for pre... the refl date is before the burn date which is specified by the burn date from the MCD64A1 dataset
# the burn date from the MCD64A1 dataset is the date of the fire, so the
# preNBR date should be before that
# <-- incline expression eval of the number of True values in each preNBR mask
print(nt1 + nt2 + nt3 + nt4 + nt5)
print(pre_nbr_masks_mod[0].shape)  # Should be (2400, 2400)

post_nbr_masks_mod = find_post_nbr_vectorized(postNBR_threshold, "MOD09A1")

# Count True values in the first MOD09A1 mask
print(post_nbr_masks_mod[0].shape)
# Count True values in the first MOD09A1 mask
print(np.sum(post_nbr_masks_mod[0]))

post_nbr_masks_myd = find_post_nbr_vectorized(postNBR_threshold, "MYD09A1")

"""
Differenced Normalized Burn Ratio (dNBR) is calculated as:
dNBR = NBR pre-fire – NBR post-fire
nbr = calculate_nbr(band_2, band_7)
nbr_pre = pre_nbr_masks_mod
nbr_post = post_nbr_masks_mod

Valid Range: −2000 to 2000 (FIRE!)
"""


def calculate_dnbr_vectorized(nbr_pre, nbr_post):
    # Convert boolean masks to float for subtraction
    calc_nbr = nbr_pre.astype(np.float32) - nbr_post.astype(np.float32)

    # Only return dNBR values within valid range (-2000 to 2000)
    calc_nbr = np.where(
        (calc_nbr >= -
         2000) & (
            calc_nbr <= 2000),
        calc_nbr,
        np.nan)

    return calc_nbr


dnbr_mod = [
    calculate_dnbr_vectorized(
        pre, post) for pre, post in zip(
            pre_nbr_masks_mod, post_nbr_masks_mod)]
dnbr_myd = [
    calculate_dnbr_vectorized(
        pre, post) for pre, post in zip(
            pre_nbr_masks_myd, post_nbr_masks_myd)]

# Print the shapes of the dNBR arrays
print(dnbr_mod)

# dNBR measures change
# RdNBR measures impact
"""
Relativized differenced Normalized Burn Ratio (RdNBR) is calculated as:
RdNBR = dNBR / sqrt(abs(NBR pre-fire / 1000))

This formula normalizes the dNBR by the pre-fire NBR value, allowing for a relative comparison of burn severity.
"""

def calculate_rdnbr_vectorized(dnbr, nbr_pre):
    # Avoid division by zero, NaN, or Inf in the denominator
    safe = (nbr_pre != 0) & (~np.isnan(nbr_pre)) & (~np.isinf(nbr_pre))
    result = np.zeros_like(dnbr, dtype=np.float32)
    result[safe] = dnbr[safe] / np.sqrt(np.abs(nbr_pre[safe] / 1000))
    return result


rdnbr_mod = [
    calculate_rdnbr_vectorized(
        pre, post) for pre, post in zip(
            dnbr_mod, pre_nbr_masks_mod)]
rdnbr_myd = [
    calculate_rdnbr_vectorized(
        pre, post) for pre, post in zip(
            dnbr_myd, pre_nbr_masks_myd)]

# Print the shapes of the RdNBR arrays
print("RdNBR MOD09A1 shapes:", [arr.shape for arr in rdnbr_mod])
print("RdNBR MYD09A1 shapes:", [arr.shape for arr in rdnbr_myd])

# Print # of  RdNBR values > 100
print("Sample RdNBR values > 100:")
for i, rdnbr in enumerate(rdnbr_mod):
    if rdnbr is not None:
        # Print first 10 values greater than 100
        print(f"MOD09A1 {i + 1}: {rdnbr[rdnbr > 10].flatten()[:10]}")

# Print sample RdNBR values which are greater than 100
print("Sample RdNBR values > 100:")
for i, rdnbr in enumerate(rdnbr_mod):
    if rdnbr is not None:
        # Print first 10 values greater than 100
        print(f"MOD09A1 {i + 1}: {rdnbr[rdnbr > 10].flatten()[:10]}")


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
            showscale=(col == 7)  # Adjust as needed
        ),
        row=row, col=col
    )
    fig.update_xaxes(showticklabels=False, row=row, col=col)
    fig.update_yaxes(showticklabels=False, row=row, col=col)

    annotations = list(fig.layout.annotations)  # convert tuple to list
    annotations.append(dict(
        x=0.5,
        y=1.1,
        xref='paper',
        yref='paper',
        text=title,
        showarrow=False,
        font=dict(size=14)
    ))
    fig.layout.annotations = annotations  # assign back

# Create a matplotlib figure to visualize the dNBR values


def add_nbr_magnitude_heatmap_to_fig(
        data,
        fig,
        row,
        col,
        overlay_mask=None,
        title="Pixel Magnitude Heatmap"):
    if not isinstance(data, np.ndarray) or data.ndim != 2:
        raise ValueError("Input must be a 2D NumPy array.")

    # Normalize to -1 to 1 range using 2000 bounds
    normed = np.clip(data / 2000.0, -1.0, 1.0)

    # Define Plotly version of 'seismic'
    seismic_colorscale = [
        [0.0, "blue"],
        [0.5, "white"],
        [1.0, "red"]
    ]

    build_heatmap(
        normed,
        title,
        colorscale=seismic_colorscale,
        row=row,
        col=col,
        fig=fig,
        overlay_mask=overlay_mask)


# Print the dNBR values within the (0.1 ~ 0.3) range // high burn severity
print("Sample dNBR values in the range (0.1 ~ 0.3):")
print(dnbr_mod[0][(dnbr_mod[0] > 0.1) & (dnbr_mod[0] < 0.3)
                  ].flatten()[:10])  # Print first 10 values

# Print total number of dNBR values in the range (0.1 ~ 0.3)
print("Total number of dNBR values in the range (0.1 ~ 0.3):",
      np.sum((dnbr_mod[0] > 0.1) & (dnbr_mod[0] < 0.3)))

# mod_hdf_date_time
# Save the dNBR heatmap to an HTML file
# Save all NBR graphics to HTML files that visualize the pixel magnitude
# heatmap
fig = make_subplots(
    rows=2,
    cols=5,
    subplot_titles=[
        f"MOD {
            i +
            1}: {
                mod_hdf_date_time[i]['start_date']} - {
                    mod_hdf_date_time[i]['end_date']}" for i in range(5)] +
    [
        f"MYD {
            i +
            1}: {
            myd_hdfs_date_time[i]['start_date']} - {
            myd_hdfs_date_time[i]['end_date']}" for i in range(5)],
    horizontal_spacing=0.03,
    vertical_spacing=0.08)

# Loop through the MOD09A1 and MYD09A1 datasets to add heatmaps
for i, entry in enumerate(bands["MOD09A1"]):
    add_nbr_magnitude_heatmap_to_fig(
        entry["nbr"],
        fig,
        row=1,
        col=i + 1,
        title=f"MOD09A1 {
            i + 1} NBR Heatmap")

for i, entry in enumerate(bands["MYD09A1"]):
    add_nbr_magnitude_heatmap_to_fig(
        entry["nbr"],
        fig,
        row=2,
        col=i + 1,
        title=f"MYD09A1 {
            i + 1} NBR Heatmap")


fig.update_layout(
    height=VISUALIZATION_HEIGHT,
    width=VISUALIZATION_WIDTH,
    title_text=f"NBR Visualizations for MYD09A1",
    showlegend=False,
    margin=dict(t=80, b=40, l=40, r=40),
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(color='white')
)

# Create NBR visualizations for MOD09A1 and MYD09A1
# nbr_vis_path = os.path.abspath(f"./data_processing/visualizations/nbr_visualization.jpeg")
st_output_name = os.path.abspath(
    f"./data_processing/streamlit_visualizations/nbr_visualization.jpeg")
# fig.write_image(nbr_vis_path)
fig.update_layout(height=STREAMLIT_VISUALIZATION_HEIGHT,
                  width=STREAMLIT_VISUALIZATION_WIDTH)
fig.write_image(st_output_name, height=STREAMLIT_VISUALIZATION_HEIGHT, width=STREAMLIT_VISUALIZATION_WIDTH)
print(f"Visualization saved to {st_output_name}")


# Print the characteristics of the dnbr_mod and dnbr_myd arrays
print("Characteristics of dnbr_mod and dnbr_myd:")
print("dnbr_mod shape:", [arr.shape for arr in dnbr_mod])
print("dnbr_myd shape:", [arr.shape for arr in dnbr_myd])


def aggregate_dnbr_array(dnbr):
    # Mask invalid values (like fill values, or NaNs)
    valid_dnbr = np.where(np.isfinite(dnbr), dnbr, np.nan)

    agg_value = np.nanmean(valid_dnbr)

    return agg_value


def aggregate_rdnbr_arrays(rdnbr):
    # Mask invalid values (like fill values, or NaNs)
    valid_rdnbr = np.where(np.isfinite(rdnbr), rdnbr, np.nan)

    agg_value = np.nanmean(valid_rdnbr)

    return agg_value


# Aggregate dNBR values for MOD09A1 and MYD09A1
dnbr_mod_agg = [aggregate_dnbr_array(nbr) for nbr in dnbr_mod]
dnbr_myd_agg = [aggregate_dnbr_array(nbr) for nbr in dnbr_myd]

print(dnbr_mod_agg)
print(dnbr_myd_agg)

rdnbr_mod_agg = [aggregate_dnbr_array(nbr) for nbr in rdnbr_mod]
rdnbr_myd_agg = [aggregate_dnbr_array(nbr) for nbr in rdnbr_myd]

print(rdnbr_mod_agg)
print(rdnbr_myd_agg)

# Create a line plot to visualize the aggregated dNBR values

def plot_dnbr_aggregated_separate(
    dnbr_mod_agg, dnbr_myd_agg, mod_hdf_date_time, myd_hdf_date_time,
    output_html_mod,
    output_html_myd,
    output_streamlit_mod,
    output_streamlit_myd
):
    # Prepare x-axis labels from "start_time" fields
    mod_x = [entry["start_date"] for entry in mod_hdf_date_time]
    myd_x = [entry["start_date"] for entry in myd_hdf_date_time]

    # MOD09A1 plot
    fig_mod = go.Figure()
    fig_mod.add_trace(go.Scatter(
        x=mod_x,
        y=dnbr_mod_agg,
        mode="lines+markers",
        name="MOD09A1 dNBR"
    ))
    fig_mod.update_layout(
        title="Fire Severity (Aggregated dNBR) for MOD09A1",
        xaxis_title="Start Time",
        yaxis_title="dNBR Value",
        template="plotly_dark"
    )
    os.makedirs(os.path.dirname(output_html_mod), exist_ok=True)
    os.makedirs(os.path.dirname(output_streamlit_mod), exist_ok=True)
    # fig_mod.write_image(output_html_mod)
    fig.update_layout(
        height=STREAMLIT_VISUALIZATION_HEIGHT,
        width=STREAMLIT_VISUALIZATION_WIDTH)
    fig_mod.write_image(output_streamlit_mod, height=STREAMLIT_VISUALIZATION_HEIGHT, width=STREAMLIT_VISUALIZATION_WIDTH)
    print(
        f"MOD09A1 Aggregated dNBR plot saved to {output_html_mod} and {output_streamlit_mod}")

    # MYD09A1 plot
    fig_myd = go.Figure()
    fig_myd.add_trace(go.Scatter(
        x=myd_x,
        y=dnbr_myd_agg,
        mode="lines+markers",
        name="MYD09A1 dNBR"
    ))
    fig_myd.update_layout(
        title="Fire Severity (Aggregated dNBR) for MYD09A1",
        xaxis_title="Start Time",
        yaxis_title="dNBR Value",
        template="plotly_dark"
    )
    os.makedirs(os.path.dirname(output_html_myd), exist_ok=True)
    os.makedirs(os.path.dirname(output_streamlit_myd), exist_ok=True)
    # fig_myd.write_image(output_html_myd)
    fig_myd.update_layout(
        height=STREAMLIT_VISUALIZATION_HEIGHT,
        width=STREAMLIT_VISUALIZATION_WIDTH)
    fig_myd.write_image(output_streamlit_myd, height=STREAMLIT_VISUALIZATION_HEIGHT, width=STREAMLIT_VISUALIZATION_WIDTH)
    print(
        f"MYD09A1 Aggregated dNBR plot saved to {output_html_myd} and {output_streamlit_myd}")


plot_dnbr_aggregated_separate(
    dnbr_mod_agg, dnbr_myd_agg, mod_hdf_date_time, myd_hdfs_date_time,
    os.path.abspath("./data_processing/visualizations/dnbr_mod_over_time.jpeg"),
    os.path.abspath("./data_processing/visualizations/dnbr_myd_over_time.jpeg"),
    os.path.abspath("./data_processing/streamlit_visualizations/dnbr_mod_over_time.jpeg"),
    os.path.abspath("./data_processing/streamlit_visualizations/dnbr_myd_over_time.jpeg")
)


def plot_rdnbr_aggregated_separate(
    rdnbr_mod_agg, rdnbr_myd_agg, mod_hdf_date_time, myd_hdf_date_time,
    output_html_mod,
    output_html_myd,
    output_streamlit_mod,
    output_streamlit_myd
):
    # Prepare x-axis labels from "start_time" fields
    mod_x = [entry["start_date"] for entry in mod_hdf_date_time]
    myd_x = [entry["start_date"] for entry in myd_hdf_date_time]

    # MOD09A1 plot
    fig_mod = go.Figure()
    fig_mod.add_trace(go.Scatter(
        x=mod_x,
        y=rdnbr_mod_agg,
        mode="lines+markers",
        name="MOD09A1 RdNBR"
    ))
    fig_mod.update_layout(
        title="Burn Severity Relative to Pre-fire Vegetation Density (Aggregated RdNBR) for MOD09A1",
        xaxis_title="Start Time",
        yaxis_title="RdNBR Value",
        template="plotly_dark")
    os.makedirs(os.path.dirname(output_html_mod), exist_ok=True)
    os.makedirs(os.path.dirname(output_streamlit_mod), exist_ok=True)
    # fig_mod.write_image(output_html_mod)
    fig_mod.update_layout(
        height=STREAMLIT_VISUALIZATION_HEIGHT,
        width=STREAMLIT_VISUALIZATION_WIDTH)
    fig_mod.write_image(output_streamlit_mod, height=STREAMLIT_VISUALIZATION_HEIGHT, width=STREAMLIT_VISUALIZATION_WIDTH)
    print(
        f"MOD09A1 Aggregated RdNBR plot saved to {output_html_mod} and {output_streamlit_mod}")

    # MYD09A1 plot
    fig_myd = go.Figure()
    fig_myd.add_trace(go.Scatter(
        x=myd_x,
        y=rdnbr_myd_agg,
        mode="lines+markers",
        name="MYD09A1 dNBR"
    ))
    fig_myd.update_layout(
        title="Burn Severity Relative to Pre-fire Vegetation Density (Aggregated RdNBR) for MYD09A1",
        xaxis_title="Start Time",
        yaxis_title="RdNBR Value",
        template="plotly_dark")
    os.makedirs(os.path.dirname(output_html_myd), exist_ok=True)
    os.makedirs(os.path.dirname(output_streamlit_myd), exist_ok=True)
    # fig_myd.write_image(output_html_myd)
    fig_myd.update_layout(
        height=STREAMLIT_VISUALIZATION_HEIGHT,
        width=STREAMLIT_VISUALIZATION_WIDTH)
    fig_myd.write_image(output_streamlit_myd, height=STREAMLIT_VISUALIZATION_HEIGHT, width=STREAMLIT_VISUALIZATION_WIDTH)
    print(
        f"MYD09A1 Aggregated RdNBR plot saved to {output_html_myd} and {output_streamlit_myd}")


plot_rdnbr_aggregated_separate(
    dnbr_mod_agg, dnbr_myd_agg, mod_hdf_date_time, myd_hdfs_date_time,
    os.path.abspath("./data_processing/visualizations/RdNBR_mod_over_time.jpeg"),
    os.path.abspath("./data_processing/visualizations/RdNBR_myd_over_time.jpeg"),
    os.path.abspath("./data_processing/streamlit_visualizations/RdNBR_mod_over_time.jpeg"),
    os.path.abspath("./data_processing/streamlit_visualizations/RdNBR_myd_over_time.jpeg")
)

print("All visualizations and aggregated plots have been saved successfully.")
