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



def RoomTypepage(app,vis):
    global btns_list
    global list_neighbours
   
    feature = "price"
    #features = ["price","minimum_nights","bathrooms","beds","accommodates","review_scores_rating"]
    group = "PORTO"
    list_neighbours = vis.all_neighbours
    ''' DASH '''

    feature_list = ["price","minimum_nights","number_of_reviews","review_scores_rating"]

    body = html.Div([
        html.H1(id = "title",
            children=["Room Type Analysis in {}".format(group)]),
        html.Div([
        html.P("Choose Group:",style={"margin-left":"1vw","font-weight": "bold"}),
        dcc.Dropdown(
            id="dropdownRT",
            options=[
                {'label': x.replace("_"," ").capitalize(), 'value': x} for x in list_neighbours
            ],
        value=group,
        clearable=False,
        style={"width":"20vw","margin-left":"1vw"},
        ),

        ],className="row",),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="six columns",
                    children=[
                        html.Div(
                            children=dcc.Graph(id="Hist",figure = vis.hist_vizualization(group,feature))
                        ),
                        html.Br(),
                        
                        html.Div(
                            className="row",
                            children=[
                                html.P("Features:",style={"margin-left":"2vw","font-weight": "bold"}),
                                dcc.RadioItems(
                                    id = 'radio_items_room_type',
                                    options=
                                        [{"label":f.replace("_"," ").capitalize(),"value":f} for f in feature_list],
                                
                                    value='price',
                                    labelStyle = {'cursor': 'pointer', 'margin-left':'20px'},
                                    #style={"margin-left":"2vw"}
                                ),
                            ]
                        ),
                        html.Div(
                            className="six columns",
                            children=html.Div(
                                
                                dcc.Graph(id="Bar",figure = vis.bar_room_type_visualization(group,feature),
                                style={'width': '100vh', 'height': '40vh',"padding-left": "4vw"},
                                ),

                            )
                        ),
                    ]
                ),
                html.Div(
                    className="six columns",
                    children=html.Div(
                        children=dcc.Graph(id="Pie",figure = vis.pie_vizualization(group,feature)),
                    )
                )
            ]
        ),
    ],style={"margin-left":"1vw"})    

   
    layout = html.Div([
    nav,
    body
    ])

   

    return layout
