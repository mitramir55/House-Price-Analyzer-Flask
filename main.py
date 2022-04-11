import re
from flask import Flask, flash, redirect, url_for, render_template, request, session
from matplotlib.pyplot import title
import numpy as np
import pandas as pd

# for the map
import os 
import folium
from folium import plugins
from datetime import date

app = Flask(__name__)

# config------------------------------------------------
DATASETS_BASE_FOLDER = 'Dataset\\'
app.config['SECRET_KEY'] = '12345'

#------------------------------------------------------


@app.route('/', methods=['POST', 'GET'])
def index(**kwargs):

    # sample map-----------------------
    df = pd.read_csv(DATASETS_BASE_FOLDER + 'Sample_scraped_data_calgary.csv')
    df_sample = df.sample(n=20).reset_index(drop=True)


    map = folium.Map(location=[51.0447, -114.0719], title='Sample rentals')
    for i in range(len(df_sample)):

        record = df_sample.loc[i]
        
        marker = [record.latitude, record.longitude]
        popup = record.type + ' - ' + str(record.price) + ' availability: ' + str(record.available_month)
        icon = folium.Icon(color="blue",icon="glyphicon glyphicon-home")
        
        folium.Marker(location=marker, popup=popup, icon=icon).add_to(map)


    map.save('templates/map.html')

    return render_template('index.html')
        

@app.route('/map')
def map():
    return render_template('map.html')