import pandas as pd

url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/c6.1/csv/MODIS_C6_1_Global_24h.csv"
df = pd.read_csv(url)
