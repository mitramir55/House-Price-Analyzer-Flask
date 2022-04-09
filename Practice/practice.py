
import regex as re
import pandas as pd
import numpy as np
from sqlalchemy import column
from termcolor import colored
from urllib.request import urlopen
import json
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# Import necessary packages
import os 
import folium
from folium import plugins
import rioxarray as rxr
import earthpy as et
import earthpy.spatial as es

# Import data from EarthPy
data = et.data.get_data('colorado-flood')

# Set working directory to earth-analytics
os.chdir(os.path.join(et.io.HOME, 'earth-analytics', 'data'))
"""

"""

json_file = pd.read_json('Dataset\prepared_map_data.json')
print(json_file)
df = pd.read_csv(r'Dataset\calgary_cleaned_rentals_dataset.csv')
df.head()
df.columns
df.rented.unique()
len(df[df.availability == 'Immediate']) / len(df)

df[df.availability != 'Immediate'].availability.unique()
df.loc[:, 'availability_month']
#df.loc[:, 'date'] = df.loc[:, 'a'].apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d'))

malformatted_dates_idx = []
for i in range(len(df)):
    try: pd.to_datetime(df.loc[i, 'a'], format='%Y-%m-%d')
    except: malformatted_dates_idx.append(i)
df.loc[malformatted_dates_idx[1], :]

len(malformatted_dates_idx)

len(df[df.price.isna()])

df.dropna(subset=['price'], inplace=True)
df.reset_index(inplace=True, drop=True)

pd.to_datetime(df.loc[2765, 'a'], format="%Y-%m-%d")