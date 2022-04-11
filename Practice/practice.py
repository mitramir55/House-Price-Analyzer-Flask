
import regex as re
import pandas as pd
import numpy as np
from sqlalchemy import column
from termcolor import colored
from urllib.request import urlopen
import json
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
df = pd.read_csv('Dataset\calgary_cleaned_rentals_dataset_3.csv')
import folium


df_sample = df.sample(n=20).reset_index(drop=True)


from datetime import date
# Create a map using Stamen Terrain, centered on Boulder, CO
map = folium.Map(location=[51.0447, -114.0719], 
               tiles = 'Stamen Terrain')

for i in range(len(df_sample)):

    record = df_sample.loc[i]
    
    marker = [record.latitude, record.longitude]
    popup = record.type + ' - ' + str(record.price) + ' availability: ' + str(record.available_month)
    icon = folium.Icon(color="blue",icon="glyphicon glyphicon-home")
    
    folium.Marker(location=marker, popup=popup, icon=icon).add_to(map)


map