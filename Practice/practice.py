"""
import regex as re
import pandas as pd
import numpy as np
from sqlalchemy import column
from termcolor import colored
from urllib.request import urlopen
import json

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

pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
df = pd.read_csv('Dataset\Sample_scraped_data_calgary.csv')
df_sample = df.sample(n=20).reset_index(drop=True)

df.isna().sum()



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
    
scrape_major_cities()

"""

import plotly.graph_objs as go
import plotly.offline as py

import pandas as pd
import numpy as np
from ipywidgets import interactive, HBox, VBox

py.init_notebook_mode()

df = pd.read_csv('https://raw.githubusercontent.com/jonmmease/plotly_ipywidget_notebooks/master/notebooks/data/cars/cars.csv')

f = go.FigureWidget([go.Scatter(y = df['City mpg'], x = df['City mpg'], mode = 'markers')])
scatter = f.data[0]
N = len(df)
scatter.x = scatter.x + np.random.rand(N)/10 *(df['City mpg'].max() - df['City mpg'].min())
scatter.y = scatter.y + np.random.rand(N)/10 *(df['City mpg'].max() - df['City mpg'].min())
scatter.marker.opacity = 0.5

def update_axes(xaxis, yaxis):
    scatter = f.data[0]
    scatter.x = df[xaxis]
    scatter.y = df[yaxis]
    with f.batch_update():
        f.layout.xaxis.title = xaxis
        f.layout.yaxis.title = yaxis
        scatter.x = scatter.x + np.random.rand(N)/10 *(df[xaxis].max() - df[xaxis].min())
        scatter.y = scatter.y + np.random.rand(N)/10 *(df[yaxis].max() - df[yaxis].min())

axis_dropdowns = interactive(update_axes, yaxis = df.select_dtypes('int64').columns, xaxis = df.select_dtypes('int64').columns)

# Create a table FigureWidget that updates on selection from points in the scatter plot of f
t = go.FigureWidget([go.Table(
    header=dict(values=['ID','Classification','Driveline','Hybrid'],
                fill = dict(color='#C2D4FF'),
                align = ['left'] * 5),
    cells=dict(values=[df[col] for col in ['ID','Classification','Driveline','Hybrid']],
               fill = dict(color='#F5F8FF'),
               align = ['left'] * 5))])

def selection_fn(trace,points,selector):
    t.data[0].cells.values = [df.loc[points.point_inds][col] for col in ['ID','Classification','Driveline','Hybrid']]

scatter.on_selection(selection_fn)

# Put everything together
VBox((HBox(axis_dropdowns.children),f,t))