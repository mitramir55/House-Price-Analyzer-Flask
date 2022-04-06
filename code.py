from bs4 import BeautifulSoup
import requests
import regex as re
import pandas as pd
import numpy as np
from termcolor import colored
from urllib.request import urlopen
import json
pd.set_option('display.max_columns', None)

# search parameters ------------------------------------------
city = 'calgary'
types = ['Apartment', 'Shared', 'Basement', 'Condo',
    'Loft', 'House', 'Main Floor', 'Townhouse']
price_ranges = [(100, 600), (600, 1000), (1000, 1500),
 (1500, 2000), (2000, 3000), (3000, 4000), (4000, 5000)]

cols_to_drop = ['phone', 'phone_2', 'f', 's', 'title',
                'intro', 'userId', 'id', 'ref_id',
                'v', 'thumb2','link', 'marker', 'preferred_contact']
    

# functions -----------------------------------------------
def get_json(url):
    url = url.replace(" ", "%20")
    response = urlopen(url)
    data_json = json.loads(response.read())
    return data_json

def convert_utilities_col(df):
    df.loc[:, 'utility_heat'] = df.loc[:, 'utilities_included'].apply(lambda x: 1 if 'Heat' in x else 0)
    df.loc[:, 'utility_electricity'] = df.loc[:, 'utilities_included'].apply(lambda x: 1 if 'Electricity' in x else 0)
    df.loc[:, 'utility_water'] = df.loc[:, 'utilities_included'].apply(lambda x: 1 if 'Water' in x else 0)
    df.loc[:, 'utility_cable'] = df.loc[:, 'utilities_included'].apply(lambda x: 1 if 'Cable' in x else 0)
    df.loc[:, 'utility_internet'] = df.loc[:, 'utilities_included'].apply(lambda x: 1 if 'Internet' in x else 0)

    df.drop(columns=['utilities_included'], inplace=True)

    return df


def scrape_data(city, types=types, price_ranges=price_ranges):
    df_total = pd.DataFrame()

    base_url = 'https://www.rentfaster.ca/api/map.json?'
    for type in types:

        url = base_url + f'cities={city}&type={type}'
        
        # scrape based on residence type
        data_json = get_json(url)
        listings = data_json['listings']
        df_subset = pd.DataFrame(listings)

        len_subset_ids = len(df_subset.id.unique())
        
        # More than 500 records!
        # Querying based on price range
        if len_subset_ids==500:
            
            for (s, e) in price_ranges:
                url = base_url + f'cities={city}&type={type}&price_range_adv[from]={s}&price_range_adv[to]={e}'

                data_json = get_json(url)
                listings = data_json['listings']
                df_subset = pd.DataFrame(listings)
                df_total = pd.concat([df_total, df_subset], axis=0)
        else:
            df_total = pd.concat([df_total, df_subset], axis=0)

    return df_total

def drop_unwanted_cols(df, cols=cols_to_drop):
    all_columns = df.columns
    for col in cols:
        if col in all_columns:
            df.drop(columns=[col], inplace=True)
    return df


df = scrape_data(city='calgary', types=types)
df = convert_utilities_col(df)
df.drop_duplicates(inplace=True)
df = drop_unwanted_cols(df)
df.fillna(0, inplace=True)
df.reset_index(drop=True, inplace=True)


df.to_csv(f'Dataset/{city}_cleaned_rentals_dataset.csv', index=False)