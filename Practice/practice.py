
import regex as re
import pandas as pd
import numpy as np
from sqlalchemy import column
from termcolor import colored
from urllib.request import urlopen
import json
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
df = pd.read_csv('Dataset\Sample_scraped_data_calgary.csv')
df_sample = df.sample(n=20).reset_index(drop=True)

df.isna().sum()