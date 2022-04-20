import regex as re
import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor

import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class RentalsAnalyzer:
    def __init__(self, df) -> None:
        self.df = df

    def overall_view(self):
        """
        give an overall view on the df by finding the minimum, maximum, average,
        and median price of properties
        """
        length = len(self.df)

        # maximum price
        prop_max_price = self.df[self.df.price==max(self.df.price)]

        price_max = prop_max_price.price
        type_max_price = prop_max_price.type

        # minimum price
        prop_min_price = self.df[self.df.price==min(self.df.price)]

        price_min = prop_min_price.price
        type_min_price = prop_min_price.type

        # mean price
        price_mean = np.round(np.mean(self.df.price), decimals=2)
        price_median = np.median(self.df.price)

        return length, price_mean, price_median, \
        price_max, type_max_price, price_min, type_min_price


    def plot_histogram(self):

        fig = px.histogram(self.df, x="price", title='Histogram of Prices',
                        color="type", marginal="box", # can be `box`, `violin`
                         hover_data=['type', 'price', 'beds', 'baths', 'community'],
                         nbins=50)

        fig.update_traces(opacity=0.7)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON


    def barplot_price_median_avg(self, group_by='type', sort_by='median_price_per_sq'):

        """
        creates a plot comparing avg and median of price in each residence type
        """

        self.df.loc[:, 'price_per_sq'] = [np.round(self.df.loc[i, 'price'] / self.df.loc[i, 'sq_feet'], decimals=2) for i in range(len(df))]
        
        # create the dataset
        df_1 = self.df.groupby([group_by]).agg({'price_per_sq': 'mean'}).rename(columns={'price_per_sq': 'avg_price_per_sq'})
        df_2 = self.df.groupby([group_by]).agg({'price_per_sq': 'median'}).rename(columns={'price_per_sq': 'median_price_per_sq'})

        df_exp = pd.concat([df_1, df_2], axis=1)

        df_exp.sort_values(by=sort_by, inplace=True)
        df_exp.reset_index(inplace=True)
        
        # plot the result
        xs = df_exp.type
        fig = go.Figure(data=[
        go.Bar(name='Median Price', x=df_exp[group_by], y=df_exp['median_price_per_sq'],
            text = df_exp['median_price_per_sq']),

        go.Bar(name='Average Price', x=df_exp[group_by], y=df_exp['avg_price_per_sq'],
            text=df_exp['avg_price_per_sq'])
        ])

        # Change the bar mode
        fig.update_layout(barmode='group', title = f'<b> Price per Square </b> based on Residence {group_by}',
                        xaxis=dict(title='Type of listing'),
                        yaxis=dict(title='Price per sq feet ($)'))

        # Customize aspect
        fig.update_traces(marker_line_color='rgb(8,48,107)',
                        marker_line_width=1.5, opacity=0.8)

        fig.update_traces(texttemplate='%{text:.3}')
                
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON



    def regression_sqfeet_price(self, group_by='type'):
        """
        regression plot based on the sq_feet of each residence option
        """
        fig = px.scatter(self.df, x="sq_feet", y="price", color=group_by, trendline="ols",
                    title=f'<b> Regression Plot of Price vs Square Feet </b> (for Each {group_by})')
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON



    def _create_encoded_df_from_column(self, col_name='community'):

        enc = OneHotEncoder()

        transformed_array = enc.fit_transform(self.df[[col_name]]).toarray()

        # example: col_name + name = 'type_condo'
        cols = [col_name + "_" + name for name in enc.categories_[0]]
        encoded_df =  pd.DataFrame(transformed_array, columns=cols)

        return encoded_df



    def _create_encoded_df(self, y_label='price'):

        """
        creates a completely encoded x dataframe for any ml algorithm
        x_cols = ['community_converted', 'type', 'beds', 'sq_feet', 'baths', 'cats',
        'dogs', 'utility_heat', 'utility_electricity', 'utility_water', 
        'utility_cable', 'utility_internet']
        """

        x_cols = [col for col in self.df.columns if col!=y_label]
        df_x = self.df.loc[:, x_cols]

        #perform one-hot encoding on columns
        encoder_df1 = self._create_encoded_df(col_name='community')
        encoder_df2 = self._create_encoded_df(col_name='type')

        #merge one-hot encoded columns back with original DataFrame
        df_x = df_x.join(encoder_df1).join(encoder_df2)
        df_x.drop(columns=['community_converted', 'type'], inplace=True)

        return df_x


    def create_feature_importance_df(self, y_label='price', top_n=20):
        
        y = self.df.loc[:, y_label]
        X = self._create_encoded_df(y_label='price')

        model = DecisionTreeRegressor()
        model.fit(X, y)

        importance = model.feature_importances_
        columns = X.columns

        importance_df = pd.DataFrame({'field': columns, 'importance': importance})
        importance_df.sort_values(by='importance').tail(top_n)

        return importance_df


    def boxplot_beds_baths_price(self):
        """
        plots the box plot of baths/beds count and price variation
        """
        fig = make_subplots(rows=1, cols=2)

        fig.add_trace(
            go.Box(x=self.df['baths'], y=self.df['price'], name='Number of Baths'),
            row=1, col=1
        )

        fig.add_trace(
            go.Box(x=self.df['beds'], y=self.df['price'], name='Number of Beds'),
            row=1, col=2
        )
        fig.update_layout(xaxis=dict(title='Type of listing'),
                        yaxis=dict(title='Price per sq feet ($)'))

        fig.update_xaxes(title_text="Num. Baths", row=1, col=1)
        fig.update_xaxes(title_text="Numb. Beds", row=1, col=2)

        # Update yaxis properties
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        #fig.update_yaxes(title_text="Price ($)", range=[40, 80], row=1, col=2)


        fig.update_layout(title_text=" <b> Price Variation </b> Based on Bath and Bedroom Count")
        fig.show()
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON



    def price_community_plot(self):

        # create a df dividing records based on column
        # showing average and median price
        column = 'community'

        df_1 = self.df.groupby([column]).agg({'price': 'mean'}).rename(columns={'price': 'avg_price'})
        df_2 = self.df.groupby([column]).agg({'price': 'median'}).rename(columns={'price': 'median_price'})
        df_3 = self.df.groupby([column]).agg({'city': 'count'}).rename(columns={'city': 'count_of_records'})

        df_exp = pd.concat([df_1, df_2, df_3], axis=1)

        sort_by = 'count_of_records'

        df_exp = df_exp.sort_values(by=sort_by).reset_index()

        # create the plot
        df_exp = df_exp[df_exp['count_of_records']>10]

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        x = df_exp['community']
        y_1 = df_exp['count_of_records']
        name_1 = 'Count of Listings'


        name_2 = 'Median price ($)'
        y_2 = df_exp['median_price']
        name_3 = 'Average Price ($)'
        y_3 = df_exp['avg_price']


        # Add traces
        fig.add_trace(
            go.Scatter(x=x, y=y_1, name=name_1, mode='markers'),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=x, y=y_2, name=name_2, mode='lines+markers'),
            secondary_y=True,
        )
        fig.add_trace(
            go.Scatter(x=x, y=y_3, name=name_3, mode='lines+markers'),
            secondary_y=True,
        )

        # Set x-axis title
        fig.update_xaxes(title_text="community")

        # Set y-axes titles
        fig.update_yaxes(title_text=f"<b>{name_1}</b>", secondary_y=False)
        fig.update_yaxes(title_text=f"<b>Price ($)</b>", secondary_y=True)

        fig.update_layout(
            title_text="<b>Price and popularity of communities</b> sorted by median price in communities with more than 10 listing",
            hovermode="x unified"
        )


        fig.update_traces(hovertemplate=None)
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON









