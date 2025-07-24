"""
Services for tinkering with the API
- Web Map Service (WMS)
- Web Feature Service (WFS)
- API
MAP_KEY limit is 5000 transactions / 10-minute interval
"""

API_KEY = '129f2263487977b03673af055f4c7165'

import requests
import pandas as pd

url = 'https://firms.modaps.eosdis.nasa.gov/mapserver/mapkey_status/?MAP_KEY=' + API_KEY
try:
  response = requests.get(url)
  data = response.json()
  df = pd.Series(data)
  trans = df['current_transactions']
  print(trans)
except:
  # possible error, wrong MAP_KEY value, check for extra quotes, missing letters
  print ("There is an issue with the query. \nTry in your browser: %s" % url)

da_url = 'https://firms.modaps.eosdis.nasa.gov/api/data_availability/csv/' + API_KEY + '/all'
df = pd.read_csv(da_url)
print(df.head())

"""
SENSOR DATA:
- MODIS_NRT
- MODIS_SP
- VIIRS_NOAA20_NRT
- VIIRS_NOAA20_SP
- VIIRS_NOAA21_NRT

# MODIS = old reliable; VIIRS = next-gen eyes.
# NRT = speed > precision (live ops), SP = calibrated & clean (science-grade).
# MODIS_NRT/SP = Terra/Aqua legacy feeds.
# VIIRS_NOAA20/21_NRT/SP = JPSS sats, sharper eyes, faster streams.
"""
def get_transaction_count() :
  count = 0
  try:
    response = requests.get(url)
    data = response.json()
    df = pd.Series(data)
    count = df['current_transactions']
  except:
    print ("Error in our call.")
  return count

tcount = get_transaction_count()
print ('Our current transaction count is %i' % tcount)

start_count = get_transaction_count()
pd.read_csv(da_url)
end_count = get_transaction_count()
print ('We used %i transactions.' % (end_count-start_count))

# Data Availability for the Available Date Range of the API Key
da_url = 'https://firms.modaps.eosdis.nasa.gov/api/data_availability/csv/' + API_KEY + '/all'
df = pd.read_csv(da_url)
print(df.head())

area_url = 'https://firms.modaps.eosdis.nasa.gov/api/area/csv/' + API_KEY + '/VIIRS_NOAA20_NRT/world/1'
start_count = get_transaction_count()
df_area = pd.read_csv(area_url)
end_count = get_transaction_count()
print ('We used %i transactions.' % (end_count-start_count))

print(df_area.head())

area_url = 'https://firms.modaps.eosdis.nasa.gov/api/area/csv/' + API_KEY + '/VIIRS_NOAA20_NRT/54,5.5,102,40/3'
df_area = pd.read_csv(area_url)
print(df_area.head())

### Countries
countries_url = 'https://firms.modaps.eosdis.nasa.gov/api/countries'
df_countries = pd.read_csv(countries_url, sep=';')
print(df_countries.head())

### Country Specific Data using the Country Code
countries_url = 'https://firms.modaps.eosdis.nasa.gov/api/countries'
df_countries = pd.read_csv(countries_url, sep=';')
print(df_countries.head())