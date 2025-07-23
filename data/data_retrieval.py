import pandas as pd
import pytz

url = "https://firms.modaps.eosdis.nasa.gov/content/notebooks/sample_viirs_snpp_071223.csv"

def get_data(url):
    """
    Fetches the data from the specified URL and returns it as a pandas DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing the data from the CSV file.
    """
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        print(f"An error occurred while fetching the data: {e}")
        return None

# Fetch the data
df = get_data(url)
print ('Rows: %i \nCols: %i' % (df.shape[0], df.shape[1]))

# Show all the column titles
print("Column Titles:")
for col in df.columns:
    print(col)

# Get unique version values
unique_versions = df['version'].unique()
print("\nUnique Version Values:")
for version in unique_versions:
    print(version)

# Show the length of each unique version column
print ('Version 2.0NRT has %i records and version 2.0URT has %i records' % (len(df[df['version']=='2.0NRT']), len(df[df['version']=='2.0URT'])))

# Crude Bounding Box Method for Obtaining Fire Data over a Specific Area

# Create a function that allows you to obtain fire data over a specific region using the bounding box method specified by the following URL:
# https://firms.modaps.eosdis.nasa.gov/active_fire/coordinates.html

regions = {
    "World": {"West": -180, "South": -90, "East": 180, "North": 90},
    "Canada": {"West": -150, "South": 40, "East": -49, "North": 79},
    "Alaska": {"West": -180, "South": 50, "East": -139, "North": 72},
    "USA (Conterminous) & Hawaii": {"West": -160.5, "South": 17.5, "East": -63.8, "North": 50},
    "Central America": {"West": -119.5, "South": 7, "East": -58.5, "North": 33.5},
    "South America": {"West": -112, "South": -60, "East": -26, "North": 13},
    "Europe": {"West": -26, "South": 34, "East": 35, "North": 82},
    "North and Central Africa": {"West": -27, "South": -10, "East": 52, "North": 37.5},
    "Southern Africa": {"West": 10, "South": -36, "East": 58.5, "North": -4},
    "Russia and Asia": {"West": 26, "South": 9, "East": 180, "North": 83.5},
    "South Asia": {"West": 54, "South": 5.5, "East": 102, "North": 40},
    "South East Asia": {"West": 88, "South": -12, "East": 163, "North": 31},
    "Australia and New Zealand": {"West": 110, "South": -55, "East": 180, "North": -10}
}

def get_fire_data(region, df):
    """
    Filters the DataFrame for fire data within the specified region's bounding box.

    Args:
        region (str): The name of the region to filter by.
        df (pd.DataFrame): The DataFrame containing fire data.

    Returns:
        pd.DataFrame: Filtered DataFrame containing fire data for the specified region.
    """
    if region not in regions:
        print(f"Region '{region}' not found.")
        return None

    bbox = regions[region]
    filtered_df = df[(df['longitude'] >= bbox['West']) &
                     (df['longitude'] <= bbox['East']) &
                     (df['latitude'] >= bbox['South']) &
                     (df['latitude'] <= bbox['North'])].copy()

    return filtered_df.reset_index(drop=True) # resetting the index of the dataset

# World
world_df = get_fire_data("World", df)
# Canada
canada_df = get_fire_data("Canada", df)
# Alaska
alaska_df = get_fire_data("Alaska", df)
# USA (Conterminous) & Hawaii
usa_df = get_fire_data("USA (Conterminous) & Hawaii", df)
# Central America
central_america_df = get_fire_data("Central America", df)
# South America
south_america_df = get_fire_data("South America", df)
# Europe
europe_df = get_fire_data("Europe", df)
# North and Central Africa
north_africa_df = get_fire_data("North and Central Africa", df)
# Southern Africa
southern_africa_df = get_fire_data("Southern Africa", df)
# Russia and Asia
russia_asia_df = get_fire_data("Russia and Asia", df)
# South Asia
south_asia_df = get_fire_data("South Asia", df)
# South East Asia
southeast_asia_df = get_fire_data("South East Asia", df)
# Australia and New Zealand
australia_df = get_fire_data("Australia and New Zealand", df)

region_dfs = {
    "World": get_fire_data("World", df),
    "Canada": get_fire_data("Canada", df),
    "Alaska": get_fire_data("Alaska", df),
    "USA (Conterminous) & Hawaii": get_fire_data("USA (Conterminous) & Hawaii", df),
    "Central America": get_fire_data("Central America", df),
    "South America": get_fire_data("South America", df),
    "Europe": get_fire_data("Europe", df),
    "North and Central Africa": get_fire_data("North and Central Africa", df),
    "Southern Africa": get_fire_data("Southern Africa", df),
    "Russia and Asia": get_fire_data("Russia and Asia", df),
    "South Asia": get_fire_data("South Asia", df),
    "South East Asia": get_fire_data("South East Asia", df),
    "Australia and New Zealand": get_fire_data("Australia and New Zealand", df)
}

print("Fire records per region:")
print(" | ".join([f"{region}: {len(dataframe)}" for region, dataframe in region_dfs.items()]))

# Custom Filters
"""
- Confidence Level
- Fire Radiative Power (FRP)
- Time of Day (N || D)
"""
df_custom_world_day = world_df[(df['confidence'] == 'h') & (df['frp'] >= 5) & (df['daynight'] == 'D')].copy()
df_custom_world_night = world_df[(df['confidence'] == 'h') & (df['frp'] >= 5) & (df['daynight'] == 'N')]

print("Custom World Day Records:", len(df_custom_world_day))
print("Custom World Night Records:", len(df_custom_world_night))

# Date Time // Time Zones
canada_df['acq_datetime'] = pd.to_datetime(canada_df['acq_date'] + ' ' + canada_df['acq_time'].astype(str).str.zfill(4), format='%Y-%m-%d %H%M')

print ('Custom World Day Data:')
canada_df['acq_datetime'].sample(5)

# TODO: timezone converisons using the pytz library

print('Canada TimeZones')
for timeZone in pytz.country_timezones['CA']:
    print(timeZone)

# Now let's see the minimum and maximum datetime range available for Canada

print ('Canada datetime value range: %s to %s' % (str(canada_df['acq_datetime'].min()), str(canada_df['acq_datetime'].max())))