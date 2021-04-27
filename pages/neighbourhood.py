# https://towardsdatascience.com/create-a-multipage-dash-application-eceac464de91

# Libraries

import os

import pandas as pd
import numpy as np
from datetime import datetime

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import geojson
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


from pages.navbar import Navbar

nav = Navbar()


global btns_list
global list_neighbours



def Neighbourhoodpage(app,vis,group):
    global btns_list
    global list_neighbours
   
    feature = "price"
    features = ["price","minimum_nights","bathrooms","beds","accommodates","review_scores_rating"]
    list_neighbours = vis.all_neighbours
    analysis = "mean"
    ''' DASH '''


    print(group,feature)
    body = html.Div([
        html.H1("{}'s Neighbourhood Airbnbs Analysis".format(group.capitalize())),
        dcc.Dropdown(
            id="dropdownN",
            options=[
                {'label': x.replace("_"," ").capitalize(), 'value': x} for x in features
                
            ],
        value=feature,
        clearable=False,),
        html.Div(
            [dbc.Button(n.capitalize(),href="/"+n) for n in list_neighbours]+[html.Div(id='container-button-timestamp')]),
        dcc.Graph(id="Map",figure = vis.map_vizualization(group,feature)),
        dcc.Graph(id="TimeSeries",figure = vis.time_series_individual(group,feature,analysis)),
    ])    

   
    layout = html.Div([
            nav,
            body,
        ])

    return layout


#vis.group_visualization_map("GONDOMAR","price")
#vis.pie_by_group_visualization("PORTO")
#vis.time_series_individual('Campanhã','price','mean')
#vis.map_pie_hist_vizualization("GONDOMAR","price")

