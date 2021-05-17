# danielgasper2006@hotmail.com 

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from pages.home import Homepage
from pages.room_type import RoomTypepage
from pages.neighbourhood import Neighbourhoodpage

from devcode.DatasetAirbnb import DatasetAirbnb
from devcode.VisualizationAirbnb import VisualizationAirbnb

import numpy as np


global btns_list
global group_analyse
global list_neighbours

ds = DatasetAirbnb("datasets")

ds.importData(calendar = True)
vis = VisualizationAirbnb(ds)


btns_list = np.zeros((len(vis.all_neighbours)),dtype=int)
list_neighbours = vis.all_neighbours
group_analyse = "PORTO"


#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(
    __name__,
    external_stylesheets=['https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/united/bootstrap.min.css']
)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])


# URL Callback
@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])

def display_page(pathname):
    global group_analyse
    if pathname == '/room_type':
        return RoomTypepage(app,vis)
    elif pathname[1:].replace("%20"," ") in list_neighbours:
        group_analyse = pathname[1:].replace("%20"," ")
        return Neighbourhoodpage(app,vis,group_analyse)
    else:
        return Homepage(app,vis)


# Room type Callbacks

@app.callback(
    Output("Pie", "figure"),
    Output("Hist", "figure"),
    Output("Bar", "figure"),
    Output("title", "children"),
    Input("dropdownRT", "value"),
    Input("radio_items_room_type", "value"),
    
)
def change_group(group,feature):
    print("Choice "+group)
    return vis.pie_vizualization(group,feature),vis.hist_vizualization(group,feature),vis.bar_room_type_visualization(group,feature),"Room Type Analysis in {}".format(group)

# Neighbourhood Callbacks

@app.callback(
    Output("Map", "figure"),
    Output("TimeSeries", "figure"),
    Input("dropdownN", "value"),
    Input("dropdownNeigh", "value"),
)
def change_group(feature,neigh):
    global group_analyse
    print("Choice "+feature)
    analysis = "mean"
    return vis.map_vizualization(group_analyse,feature),vis.time_series_individual(neigh,"price",group_analyse)

# Home Callbacks

@app.callback(
        Output("MainMap", "figure"),
        Output("ScatterMap", "figure"),
        Input("dropdown", "value"),
        Input("radio_items", "value"),
    )
def change_feature(feature,detailed):
    print("Map "+feature)
    if detailed == "False":
        return vis.main_visualization_map(feature),vis.main_visualization_list(feature)
    else:
        return vis.main_visualization_map(feature,True),vis.main_visualization_list(feature,True)


if __name__ == '__main__':
    app.run_server(debug=True)