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
    neighbourhoods = list(vis.Airbnb_complete[vis.Airbnb_complete["neighbourhood_group"]==group]["neighbourhood"].unique())
    analysis = "mean"
    feature_list = ["price","minimum_nights"]

    ''' DASH '''

    print(group,feature)
    body = html.Div([
        html.H1("{}'s Neighbourhood Group Airbnbs Analysis".format(group.capitalize())),
        
        html.Div(
            className="row",
            children=[
                html.Div(className="six columns",
                    children=[
                            html.H5("Features",style={"margin-left":"2vw","font-weight": "bold"}),                        dcc.Dropdown(
                            id="dropdownN",
                            options=[
                                {'label': x.replace("_"," ").capitalize(), 'value': x} for x in features    
                            ],
                            value=feature,
                            clearable=False,
                            style={"max-width":"10vw","margin-left":"1vw"},
                        ),
                        dcc.Graph(id="Map",figure = vis.map_vizualization(group,feature),
                        style={"width":"49vw","margin-left":"1vw"}),
                    ]
                ),
                html.Div(className="six columns",
                    children=[
                        html.H5("Neighbourhoods in {}".format(group.capitalize()),style={"margin-left":"2vw","font-weight": "bold"}),
                        dcc.Dropdown(
                            id="dropdownNeigh",
                            options=[
                                {'label': x.replace("_"," ").capitalize(), 'value': x} for x in neighbourhoods    
                            ],
                            value=neighbourhoods[0],
                            clearable=False,
                            style={"max-width":"30vw","margin-left":"1vw"},
                        ),
                        html.Br(),
                        html.Div(
                            className="row",
                            children=[
                                html.P("Features",style={"margin-left":"2vw","font-weight": "bold"}),
                                dcc.RadioItems(
                                    id = 'radio_items_room_type',
                                    options=
                                        [{"label":f.replace("_"," ").capitalize(),"value":f} for f in feature_list],
                                
                                    value='price',
                                    style={"margin-left":"2vw"},
                                    labelStyle = {"padding-right": "1vw",},
                                ),
                            ],
                        ),
                        dcc.Graph(id="TimeSeries",figure = vis.time_series_individual(neighbourhoods[0],feature,analysis),
                        style={"width":"49vw","margin-left":"1vw"}),
                    ]
                )
            ],
        ),
        
        
        # html.Div(
        #     [dbc.Button(n.capitalize(),href="/"+n) for n in list_neighbours]+[html.Div(id='container-button-timestamp')]    
        # ),
        
    ])    

   
    layout = html.Div([
            nav,
            body,
        ])

    return layout
