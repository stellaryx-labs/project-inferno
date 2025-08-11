:<<'COMMENT'
Ensures PEP8 compilance with autopep8
Aggression Level:
  --aggressive --aggressive: 2x aggressive formatting
File Configuration:
  --in-place: Modify files in place (aka do not create a backup file)
COMMENT

#!/bin/bash

echo "Starting PEP8 formatting with autopep8..."

data_processing_scripts=(
    './data_processing/hdf_extraction.py'
    './data_processing/MCD64A1_date_extraction.py'
    './data_processing/data_masking.py'
    './data_processing/dnbr_rdnbr_calc.py'
)

echo "1 . Formatting Data Pipeline Python scripts for PEP8 compliance..."

for script in "${data_processing_scripts[@]}"; do
    echo "Formatting $script with autopep8..."
    autopep8 --in-place --aggressive --aggressive "$script"
done

streamlit_scripts=(
    './app.py'
    './services/firms.py'
    './pages/about.py'
    './pages/home.py'
    './pages/severity.py'
    './config.py'
)

echo "2 . Formatting Streamlit Python scripts for PEP8 compliance..."
for script in "${streamlit_scripts[@]}"; do
    echo "Formatting $script with autopep8..."
    autopep8 --in-place --aggressive --aggressive "$script"
done

echo "Finished running script!"