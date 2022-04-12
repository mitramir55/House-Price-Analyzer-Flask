from msilib.schema import Class
import regex as re
import pandas as pd
import numpy as np
from urllib.request import urlopen
import json
pd.set_option('display.max_columns', None)


class RentalDataCollector:
    def __init__(self, city='calgary', min_price = 100, max_price = 5000,
    types = ['Apartment', 'Shared', 'Basement', 'Condo', 'Loft', 'House',
     'Main Floor', 'Townhouse'], search_leap = 100) -> None:


        self.city = city    
        self.min_price = min_price
        self.max_price = max_price
        self.types = types
        self.search_leap = search_leap
        self.cols_to_drop = [
            'phone', 'phone_2', 'f', 's', 'title', 'city','intro', 'userId',
             'id', 'ref_id', 'email', 'v', 'thumb2', 'marker',
              'preferred_contact'
              ]

        self.types = [
            'Apartment', 'Shared', 'Basement', 'Condo', 'Loft', 'House',
             'Main Floor', 'Townhouse'
             ]

    def get_json(self, url):
        url = url.replace(" ", "%20")
        response = urlopen(url)
        data_json = json.loads(response.read())
        return data_json

    def convert_utilities_col(self, df):
        df.loc[:, 'utility_heat'] = df.loc[:, 'utilities_included'].apply(lambda x: 1 if 'Heat' in x else 0)
        df.loc[:, 'utility_electricity'] = df.loc[:, 'utilities_included'].apply(lambda x: 1 if 'Electricity' in x else 0)
        df.loc[:, 'utility_water'] = df.loc[:, 'utilities_included'].apply(lambda x: 1 if 'Water' in x else 0)
        df.loc[:, 'utility_cable'] = df.loc[:, 'utilities_included'].apply(lambda x: 1 if 'Cable' in x else 0)
        df.loc[:, 'utility_internet'] = df.loc[:, 'utilities_included'].apply(lambda x: 1 if 'Internet' in x else 0)

        df = df.drop(columns=['utilities_included'])

        return df


    def scrape_data(self):
        df_total = pd.DataFrame()

        base_url = 'https://www.rentfaster.ca/api/map.json?'
        for type in self.types:

            url = base_url + f'cities={self.city}&type={self.type}&price_range_adv[from]={self.min_price}&price_range_adv[to]={self.max_price}'
            
            # scrape based on residence type
            data_json = self.get_json(url)
            listings = data_json['listings']
            df_subset = pd.DataFrame(listings)

            len_subset_ids = len(df_subset.id.unique())
            
            # More than 500 records!
            # Querying based on price range to get 
            if len_subset_ids==500:
                
                for s in range(self.min_price, self.max_price, self.search_leap):
                    url = base_url + f'cities={self.city}&type={self.type}&price_range_adv[from]={s}&price_range_adv[to]={s+self.search_leap}'

                    data_json = self.get_json(url)
                    listings = data_json['listings']
                    df_subset = pd.DataFrame(listings)
                    df_total = pd.concat([df_total, df_subset], axis=0)
            else:
                df_total = pd.concat([df_total, df_subset], axis=0)

        return df_total

    def drop_unwanted_cols(self, df):
        
        all_columns = df.columns
        for col in self.cols_to_drop:
            if col in all_columns:
                df = df.drop(columns=[col])
        return df

    def keep_not_rented(self, df):
        df = df[df['rented']=='Not-Rented']
        df = df.drop(columns=['rented'])
        return df


    def handle_second_rentals(self, df, info_cols = ['price', 'sq_feet', 'beds', 'baths']):
        """
        separates residence options that has two listings
        creates the second dataset
        then renames both dataset's cols to have info_cols names
        """
        info_cols_2 = [col + '2' for col in info_cols]

        # check for where at least two second house columns are not null
        df_second = df[(~df[info_cols_2[0]].isna())&(~df[info_cols_2[1]].isna())]

        df_second = df_second.drop(columns=info_cols)
        for col in info_cols:
            df_second = df_second.rename(columns={col + '2': col})

        df = df.drop(columns=info_cols_2)

        df_total = pd.concat([df, df_second], axis=0)
        df_total = df_total.reset_index(drop=True)

        return df_total

    def convert_date_col(self, df, null_substitute = 'call for availability'):
        """
        call for availability is represented as 3000-01-01 in the dataset
        so we replace these dates with a string
        """
        for i in range(len(df)):
            try: 
                df.loc[i, 'a'] = pd.to_datetime(df.loc[i, 'a'], format='%Y-%m-%d')
            except: 
                df.loc[i, 'a'] = null_substitute
                df.loc[i, 'availability'] = null_substitute
        df.reset_index(inplace=True, drop=True)
        return df


    def create_month_col(self, df):
        """ for analysis and filtering the results """
        for i in range(len(df)):
            try:
                df.loc[i, 'available_month'] = int(df.loc[i, 'a'].month)
            except:
                # if the value is 3001 meaning that it might be available
                df.loc[i, 'available_month'] = df.loc[i, 'a']
                
        return df


    def clean_baths_col(self, df):
        for i in range(len(df)):
            # some have 1.5 baths
            # we convert all to integer
            try: df.loc[i, 'baths'] = np.floor(float(df.loc[i, 'baths']))
            except: 
                df.loc[i, 'baths'] = 0
        return df



    def clean_beds_col(self, df):

        for i in range(len(df)):
            val = df.loc[i, 'beds']

            try: df.loc[i, 'beds'] = int(val)
            except: 
                # if there isn't a single int
                try: df.loc[i, 'beds'] = int(re.findall('\d', val)[0])
                except: df.loc[i, 'beds'] = 0
        return df

        
    def clean_sq_feet_col(self, df, remove_longer_than=50):

        unwanted = []
        for i in range(len(df)):
            record = df.loc[i, 'sq_feet']

            try:
                df.loc[i, 'sq_feet'] = int(float(record))
                

            except:
                # lengthy descriptions
                if len(record)>remove_longer_than or not re.findall('\d+', record):
                    unwanted.append(i)

                # it is 700-800 balcony
                elif re.findall('[\w\.\!\- ]*\d+ *- *\d+[\w\.\!\- ]*', record):
                    num1 = re.findall('\d+', record)[0]
                    num2 = re.findall('\d+', record)[1]

                    df.loc[i, 'sq_feet'] = int((int(num1) + int(num2))/2)

                # it is 700 + 500 balcony
                elif re.findall('[\w\.\!\- ]*\d+ *\+ *\d+[\w\.\!\- ]*', record):
                    num1 = re.findall('\d+', record)[0]
                    num2 = re.findall('\d+', record)[1]

                    df.loc[i, 'sq_feet'] = int(num1) + int(num2)

                # ~600
                elif len(re.findall('\d+', record))==1:
                    df.loc[i, 'sq_feet'] = int(re.findall('\d+', record)[0])

                # 2,000
                elif re.findall('\d+,*\d+', record):
                    df.loc[i, 'sq_feet'] = int(re.findall('\d+,*\d+', '2,000')[0].replace(',', ''))

                else:
                    unwanted.append(i)
                    
        df.drop(unwanted, inplace=True)
        df = df[df.sq_feet!=0]
        df.reset_index(inplace=True, drop=True)

        return df

    def collect_data(self):

        # filtering what we want
        df = self.scrape_data()
        df = self.drop_unwanted_cols(df)
        df = self.keep_not_rented(df)
        df.dropna(subset=['price', 'sq_feet'], how='all', inplace=True)

        # create new columns and rows
        df = self.convert_utilities_col(df)
        df = self.handle_second_rentals(df)
        df = self.convert_date_col(df, null_substitute = 'call for availability')
        df = self.create_month_col(df)

        # cleaning columns and handling types
        df = self.clean_baths_col(df)
        df = self.clean_beds_col(df)
        df = self.clean_sq_feet_col(df)
        df.loc[:, 'cats'] = df.loc[:, 'cats'].apply(lambda x : int(x))
        df.loc[:, 'dogs'] = df.loc[:, 'dogs'].apply(lambda x : int(x))


        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df


#df.to_csv(f'Dataset/{city}_cleaned_rentals_dataset_3.csv', index=False)