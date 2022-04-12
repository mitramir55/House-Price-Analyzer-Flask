import re
import types
from flask import Flask, flash, redirect, url_for, render_template, request, session
from matplotlib.pyplot import title
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests

# for the map
import os 
import folium
from folium import plugins
import datetime as dt
from datetime import date
from Rentalscraper import RentalDataCollector

app = Flask(__name__)

# config------------------------------------------------
DATASETS_BASE_FOLDER = r"Dataset/"
app.config['SECRET_KEY'] = '12345'

#------------------------------------------------------

def scrape_major_cities():

    url = 'https://www.rentfaster.ca/cities/'

    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')

    # get all elements with class = major-city
    major_cities = []

    for x in soup.find_all("li", { "class" : "major-city" }):
        scraped = x.get_text().strip()
        city = re.sub(' *\(\d+\) *', '', scraped)
        major_cities.append(city)

    return major_cities


def create_marker_properties(df, i):

    record = df.loc[i]
    
    marker_loc = [record.latitude, record.longitude]
    try:
        datetime_object = dt.datetime.strptime(record.available_month, "%m")
        month_available = datetime_object.strftime("%B")
    except: month_available='call for availability'

    popup = record.type + '\nPrice:' + str(record.price) + '\nAvailability: ' + month_available
    icon = folium.Icon(color="blue",icon="glyphicon glyphicon-home")
    return marker_loc, popup, icon

@app.route('/', methods=['POST', 'GET'])
def index(**kwargs):

    # sample map-----------------------
    df = pd.read_csv(DATASETS_BASE_FOLDER + 'Sample_scraped_data_calgary.csv')
    df_sample = df.sample(n=20).reset_index(drop=True)

    center_loc = [51.0447, -114.0719]
    map = folium.Map(location=center_loc, title='Sample rentals')

    for i in range(len(df_sample)):

        marker_loc, popup, icon = create_marker_properties(df_sample, i) 
        folium.Marker(location=marker_loc, popup=popup, icon=icon).add_to(map)


    map.save('templates/map.html')
    return render_template('index.html')
        

@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/preview', methods=['POST', 'GET'])
def index(**kwargs):

    # sample map-----------------------
    df = pd.read_csv(DATASETS_BASE_FOLDER + 'Sample_scraped_data_calgary.csv')


    return render_template('index.html')

    
@app.route('/test', methods=['POST', 'GET'])
def index(**kwargs):

    
    major_cities = scrape_major_cities()

    collector = RentalDataCollector(types=types, city=city, min_price=min_price,
    max_price=max_price)
    collector.collect_data()

    # sample map-----------------------
    df = pd.read_csv(DATASETS_BASE_FOLDER + 'Sample_scraped_data_calgary.csv')
    df.to_csv(f'Dataset/{city}_cleaned_rentals_dataset.csv', index=False)

    return render_template('index.html')