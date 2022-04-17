import regex as re
import pandas as pd
import numpy as np
import plotly.express as px

import json
import plotly
import plotly.express as px
import plotly.graph_objects as go


class RentalsAnalyzer:
    def __init__(self, df) -> None:
        self.df = df

    def plot_histogram(self):

        fig = px.histogram(self.df, x="price", title='Histogram of Prices',
                        color="type", marginal="box", # can be `box`, `violin`
                         hover_data=['type', 'price', 'beds', 'baths', 'community'],
                         nbins=50)

        fig.update_traces(opacity=0.7)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return graphJSON