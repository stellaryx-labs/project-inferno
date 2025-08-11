#!/bin/bash

SECONDS=0

# Detect Python interpreter
PYTHON=$(which python3 2>/dev/null || which python)

# Step 1: Extract HDF file fields
echo "Step 1: Extracting HDF file fields..."
$PYTHON ./data_processing/hdf_extraction.py

# Step 2: Extract burn date and uncertainty from MCD64A1
echo "Step 2: Extracting burn date and uncertainty from MCD64A1..."
$PYTHON ./data_processing/MCD64A1_date_extraction.py

# Step 3: Apply masks to MOD09A1 and MYD09A1 datasets
echo "Step 3: Masking MOD09A1 scenes..."
for i in {0..4}; do
    $PYTHON ./data_processing/data_masking.py MOD09A1 $i
done

echo "Step 3: Masking MYD09A1 scenes..."
for i in {0..4}; do
    $PYTHON ./data_processing/data_masking.py MYD09A1 $i
done

# Step 4: Calculate dNBR and RdNBR visualizations
echo "Step 4: Calculating dNBR and RdNBR visualizations..."
$PYTHON ./data_processing/dnbr_rdnbr_calc.py

echo "Pipeline complete!"
echo "Total runtime: ${SECONDS} seconds"