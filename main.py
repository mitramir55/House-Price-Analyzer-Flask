import re
import types
from cherrypy import url
from flask import Flask, flash, redirect, url_for, render_template, request, session
from graphviz import render
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

from sympy import minpoly
from Rentalscraper import RentalDataCollector
from RentalsAnalyzer import RentalsAnalyzer
app = Flask(__name__)

# config------------------------------------------------
DATASETS_BASE_FOLDER = r"Dataset/"
OUTPUT_FOLDER = r'Practice/Datasets/'
app.config['SECRET_KEY'] = '12345'

#------------------------------------------------------

def scrape_major_cities():

    url = 'https://www.rentfaster.ca/cities/'

    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')

    # get all elements with class = major-city
    major_cities = []

    # we look into href of each major city and take out the
    # name for the query
    for x in soup.find_all("li", { "class" : "major-city" }):
        link = x.find('a', href=True)['href']
        city = re.findall("\w+\/(.*)\/", link)[0]
        major_cities.append(city)

    return major_cities

major_cities = scrape_major_cities()


def determine_min_max(min_price, max_price):
    
    if max_price=='': max_price=5000 
    else: pass
    if min_price=='': min_price=0
    else: pass

    return int(min_price), int(max_price)


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


all_types = ['Apartment', 'Loft', 'House', 'Townhouse', 'Mobile',
    'Vacation', 'Storage', 'Shared', 'Duplex', 'Main Floor', 
    'Basement', 'Condo']

@app.route('/', methods=['POST', 'GET'])
def index(**kwargs):

    if request.method == 'POST':
        if request.form["submit"] == "Try it!":

            return redirect(
                url_for('inputs', enumerate=enumerate, major_cities=major_cities, types=types)
                )

    else: 
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

    
@app.route('/inputs', methods=['POST', 'GET'])
def inputs(**kwargs):

    if request.method == 'POST':
        
        types_selected = request.form.getlist('types_name')
        city = str(request.form.get('city'))
        min_price, max_price = determine_min_max(min_price=request.form.get('min'),
         max_price=request.form.get('max'))

        # check boxes
        if not types:
            flash ("Please select at least one type.")
            return render_template('inputs.html', enumerate=enumerate,
         major_cities=major_cities, types=all_types)

        if not city:
            flash ("Please select the city.")
            return render_template('inputs.html', enumerate=enumerate,
         major_cities=major_cities, types=all_types)

        session['city'] = city
        session['types'] = types_selected
        session['min_price'] = min_price
        session['max_price'] = max_price

        # all will be in the analysis page---
        collector = RentalDataCollector(types=types_selected, city=city,
         min_price=min_price, max_price=max_price)
        df = collector.collect_data()
        if len(df)==0:
            flash ("Didn't find any residence option. Try adding some more types.")
            return render_template('inputs.html', enumerate=enumerate,
            major_cities=major_cities, types=all_types)

        else:
            
            df.to_csv(OUTPUT_FOLDER + f"{session['city']}.csv", index=False)
            return redirect(url_for('analysis'))
    else:
        return render_template('inputs.html', enumerate=enumerate,
         major_cities=major_cities, types=all_types)
        

@app.route('/preview', methods=['POST', 'GET'])
def preview(**kwargs):
    return render_template('analysis.html')

@app.route('/analysis', methods=['POST', 'GET'])
def analysis(**kwargs):

    # sample map-----------------------
    df = pd.read_csv(OUTPUT_FOLDER + f"{session['city']}.csv")
    df.dropna(inplace=True)
    df.reset_index(inplace=True, drop=True)
    analyzer = RentalsAnalyzer(df)

    # plots
    histogramJSON = analyzer.plot_histogram()
    barplot_avg_median_JSON = analyzer.barplot_price_median_avg()
    regression_sqfeet_price_JSON = analyzer.regression_sqfeet_price()
    boxplot_beds_baths_price_JSON = analyzer.boxplot_beds_baths_price()
    price_community_plot_JSON = analyzer.price_community_plot()

    # dataframe
    feature_importance_df = analyzer.create_feature_importance_df()

    return render_template('analysis.html',
    zip=zip, 
     histogramJSON=histogramJSON,
     barplot_avg_median_JSON=barplot_avg_median_JSON,
     regression_sqfeet_price_JSON=regression_sqfeet_price_JSON,
     column_names=feature_importance_df.columns.values, 
     boxplot_beds_baths_price_JSON=boxplot_beds_baths_price_JSON,
     price_community_plot_JSON=price_community_plot_JSON,
     row_data=list(feature_importance_df.values.tolist()),
     )
