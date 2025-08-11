import re
from pyhdf.SD import SD, SDC
import os

"""
SCRIPT USAGE:
python hdf_extraction.py

This script extracts metadata and data attributes from HDF files, specifically focusing on MODIS and MYD09A1 datasets

Specifically, field names for the following field names:
- Date / Time
- Reflectance Band Ranges
"""

# SAMPLE RANGE / DATE - TIME
"""
  GROUP                  = RANGEDATETIME

    OBJECT                 = RANGEBEGINNINGTIME
      NUM_VAL              = 1
      VALUE                = "00:00:00.000000"
    END_OBJECT             = RANGEBEGINNINGTIME

    OBJECT                 = RANGEENDINGTIME
      NUM_VAL              = 1
      VALUE                = "23:59:59.000000"
    END_OBJECT             = RANGEENDINGTIME

    .... (other data objects) ....

  END_GROUP              = RANGEDATETIME
"""

# SAMPLE Land Surface Reflectance RANGE derived from the following
# attributes for a single band out of 1 - 7
"""
'_FillValue': -28672, 'long_name': 'Surface_reflectance_for_band_4', 'units': 'reflectance', 'valid_range': [-100, 16000], 'scale_factor': 0.0001, 'scale_factor_err': 0.0, 'add_offset': 0.0, 'add_offset_err': 0.0, 'calibrated_nt': 5}
"""

# DICT TO HOLD ALL HDF DATA
total_hdfs = {
    "MOD09A1": [
        "MOD09A1.A2024361.h08v05.061.2025004043815.hdf",
        "MOD09A1.A2025001.h08v05.061.2025011011329.hdf",
        "MOD09A1.A2025009.h08v05.061.2025022121649.hdf",
        "MOD09A1.A2025017.h08v05.061.2025030194108.hdf",
        "MOD09A1.A2025025.h08v05.061.2025035205729.hdf"
    ],
    "MYD09A1": [
        "MYD09A1.A2024361.h08v05.061.2025004044306.hdf",
        "MYD09A1.A2025001.h08v05.061.2025011010006.hdf",
        "MYD09A1.A2025009.h08v05.061.2025021213258.hdf",
        "MYD09A1.A2025017.h08v05.061.2025030194429.hdf",
        "MYD09A1.A2025025.h08v05.061.2025035182945.hdf"
    ]
}

# Create paths for each HDF file (input = DICT)


def create_paths(hdf_dict):
    paths = []
    for key, files in hdf_dict.items():
        for file in files:
            paths.append(f"/{key}/{file}")
    return paths


def extract_data_attributes(hdf_file_path):
    f = SD(hdf_file_path, SDC.READ)
    metadata = f.attributes()["CoreMetadata.0"]
    return metadata


def extract_keys(hdf_file_path):
    hdf = SD(hdf_file_path, SDC.READ)
    return hdf, hdf.datasets().keys()


def extract_em_range(hdf, hdf_keys):
    ranges_attr_list = {
        "Surface_reflectance_for_band_1": "sur_refl_b01",
        "Surface_reflectance_for_band_2": "sur_refl_b02",
        "Surface_reflectance_for_band_3": "sur_refl_b03",
        "Surface_reflectance_for_band_4": "sur_refl_b04",
        "Surface_reflectance_for_band_5": "sur_refl_b05",
        "Surface_reflectance_for_band_6": "sur_refl_b06",
        "Surface_reflectance_for_band_7": "sur_refl_b07"
    }
    em_ranges = {
        "sur_refl_b01": None,
        "sur_refl_b02": None,
        "sur_refl_b03": None,
        "sur_refl_b04": None,
        "sur_refl_b05": None,
        "sur_refl_b06": None,
        "sur_refl_b07": None
    }

    for sds_name in hdf_keys:
        sds = hdf.select(sds_name)
        attrs = sds.attributes()

        cur_attr_name = ""
        for attr in attrs:
            if attr is not None:
                if attr == 'long_name' and attrs[attr] in ranges_attr_list.keys(
                ):
                    cur_attr_name = attrs[attr]

                if attr == 'valid_range':
                    em_range_name = ranges_attr_list.get(cur_attr_name)
                    if em_range_name is not None:
                        em_ranges[em_range_name] = attrs['valid_range']

    return em_ranges


def extract_range_data(contents):
    # Isolate RANGEDATETIME block
    match = re.search(
        r'GROUP\s+=\s+RANGEDATETIME(.*?)END_GROUP\s+=\s+RANGEDATETIME',
        contents,
        re.DOTALL)
    if not match:
        return {}

    range_block = match.group(1)

    # Find all OBJECT blocks within the range block
    objects = re.findall(
        r'OBJECT\s+=\s+(\w+)(.*?)END_OBJECT\s+=\s+\1',
        range_block,
        re.DOTALL)

    result = {}
    for name, body in objects:
        # Extract VALUE from body
        val_match = re.search(r'VALUE\s+=\s+"(.*?)"', body)
        if val_match:
            result[name] = val_match.group(1)

    return result


def pretty_print_em_ranges(em_ranges):
    print("  Band Reflectance Ranges:")
    for band, range_values in em_ranges.items():
        if range_values:
            print(f"    {band}: {range_values}")
        else:
            print(f"    {band}: [No valid range]")


def pretty_print_range_data(range_data):
    print("  Date/Time Range:")
    for key, value in range_data.items():
        print(f"    {key:<20}: {value}")


def analyze_hdf(hdf_file_path):
    metadata = extract_data_attributes(hdf_file_path)
    range_data = extract_range_data(metadata)
    pretty_print_range_data(range_data)


paths = create_paths(total_hdfs)

for path in paths:
    total_path = os.path.abspath(f"./data_processing/{path}")
    print("=" * 60)
    print(f"File: {total_path}")
    analyze_hdf(total_path)
    hdf, keys = extract_keys(total_path)
    em_ranges = extract_em_range(hdf, keys)
    pretty_print_em_ranges(em_ranges)
    print()
