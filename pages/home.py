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



def Homepage(app,vis):
    global btns_list
    global list_neighbours
    
    feature = "price"
    features = ["price","minimum_nights","bathrooms","beds","accommodates","review_scores_rating"]

    btns_list = np.zeros((len(vis.all_neighbours)),dtype=int)
    list_neighbours = vis.all_neighbours
    count_neighbourhoods = vis.count_neighbourhoods
    count_neighbourhoods_percentage = vis.count_neighbourhoods_percentage
    ''' DASH '''
    body = html.Div([
        #html.H1("Porto's Airbnbs Analysis"),
        html.Br(),
        html.Div(className="row",
            children=[html.Div(className="container",
                #[dbc.Button(n.capitalize(),href="/"+n,className="btn btn-primary") for n in list_neighbours]+[html.Div(id='container-button-timestamp')]
                children=[
                    dbc.Card([
                        dbc.CardHeader(dcc.Link(n.capitalize(),href="/"+n,style={"color":"black"}),
                        style={"border-radius":"25%","height": "4vw"}), 
                        dbc.CardBody([
                            html.P("{} Airbnbs".format(count_neighbourhoods[n])),
                            html.P("{}%".format(count_neighbourhoods_percentage[n]),style={'fontWeight': 'bold'}),
                        ])
                    ],
                    className="card border-danger mb-3",
                    style={"margin-left":"1vw","width":"10vw","heigh":"10vw","border-radius":"15%"}
                    ) for n in list_neighbours],
                style={"max-width": "100vw","text-align":"center","display":"flex","flex-direction":"row"},
            ),],
            style = {"flex-direction":"row"}
        ),
        html.Br(),
        html.Div(
            className="row",
            children=[
                html.Div(className="two columns",
                    children=[
                        html.H4("Features:",
                        style={"margin-left":"2vw","font-weight": "bold"},
                        
                        ),
                        html.Div(className="column",
                        children=[
                            dcc.Dropdown(
                                id="dropdown",
                                options=[
                                    {'label': x.replace("_"," ").capitalize(), 'value': x} for x in features  
                                ],
                                value=feature,
                                clearable=False,
                                style={"max-width":"10vw","margin-left":"1vw"},
                            ),
                            dcc.RadioItems(
                                    id = 'radio_items',
                                    options=[
                                        {'label': 'By Neighbourhood Group', 'value': "False"},
                                        {'label': 'By Neighbourhood', 'value': "True"},
                                        
                                    ],
                                    value='False',
                                    style={"margin-left":"2vw","display":"inline-grid","padding":"1vw"}
                            ),  
                        ]
                        
                    ),
                    ]

                ),
                html.Div(
                    className="five columns",
                    children=html.Div(
                        children=dcc.Graph(id="MainMap",figure = vis.main_visualization_map(feature),
                        style={'width': '80vh', 'height': '70vh'}
                        ),
                    ),
                    style={"heigh":"70vw"}

                ),
                html.Div(
                    className="five columns",
                    children=html.Div(
                            children=dcc.Graph(id="ScatterMap",figure = vis.main_visualization_list(feature),
                            style={'width': '80vh', 'height': '70vh'}
                            ),
                        ),
                    style={"heigh":"70vw"}
                ),
            ],
        ),
        #dcc.Graph(id="MainMap",figure = vis.main_visualization_map(feature),
        #style={"max-width":"60vw"}),
        #dcc.Graph(id="ScatterMap",figure = vis.main_visualization_list(feature)),
    ])    

        
    layout = html.Div([
    nav,
    body
    ])

    return layout


#vis.group_visualization_map("GONDOMAR","price")
#vis.pie_by_group_visualization("PORTO")
#vis.time_series_individual('Campanhã','price','mean')
#vis.map_pie_hist_vizualization("GONDOMAR","price")

