import re
from flask import Flask, flash, redirect, url_for, render_template, request, session
import numpy as np
import pandas as pd

# for the map
import os 
import folium
from folium import plugins
import rioxarray as rxr
import earthpy as et
import earthpy.spatial as es

app = Flask(__name__)

# config------------------------------------------------
DATASETS_BASE_FOLDER = 'Dataset\\'
app.config['SECRET_KEY'] = '12345'

#------------------------------------------------------


@app.route('/', methods=['POST', 'GET'])
def index(**kwargs):
    map = folium.Map(location=[51.0447, -114.0719])
    map.save('templates/map.html')

    return render_template('index.html')
        
