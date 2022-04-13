
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