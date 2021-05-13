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

from devcode.DatasetAirbnb import DatasetAirbnb

class VisualizationAirbnb:
    def __init__(self, datasetClass):
        self.porto_view_lat = 41.1
        self.porto_view_lon = -8.638613
        self.porto_view_zoom = 8

        self.Airbnb_complete = datasetClass.Airbnb_complete
        self.Airbnb_dropna = datasetClass.Airbnb_dropna
        self.calendar = datasetClass.calendar
        self.geojson_airbnb = datasetClass.data_files["neighbourhoods.geojson"]
        self.neighbourhood_group_list = datasetClass.data_files["neighbourhood_group_list.json"]
        
        self.neighbourhood_mean = None
        self.neighbourhood_group_mean = None
        self.neighbourhood_mean = None
        self.main_visualization = None

        count = self.Airbnb_complete.groupby(["neighbourhood_group"]).count().id

        self.count_neighbourhoods = count.to_dict()
        self.count_neighbourhoods_percentage = (round(count/count.sum()*100,2)).to_dict()


        self.all_neighbours = [elem["name"] for elem in self.neighbourhood_group_list]
        self._generate_auxliar_dataframes()
        
    # Private

    def _get_info_from_json(self,name):
            for elem in self.neighbourhood_group_list:
                if elem["name"] == name:
                    return elem
            return None
    
    def _generate_auxliar_dataframes(self):
        self.neighbourhood_mean = self.Airbnb_complete.groupby("neighbourhood").mean().reset_index()
        self.neighbourhood_group_mean = self.Airbnb_complete.groupby("neighbourhood_group").mean().reset_index()
        self.main_visualization = self.neighbourhood_group_mean.join(self.Airbnb_complete[["neighbourhood_group","neighbourhood"]].set_index("neighbourhood_group"),on="neighbourhood_group")
        self.main_visualization_detailed = self.Airbnb_complete.groupby("neighbourhood").mean().reset_index()


       

    def _group_visualization_map_code(self,neighbourhood_group_name,feature):

        neighbourhood_in_group = self.Airbnb_complete[self.Airbnb_complete["neighbourhood_group"]==neighbourhood_group_name].groupby("neighbourhood").mean().reset_index()
        neighbourhood_in_group["Number of Airbnbs"]=list(self.Airbnb_complete[self.Airbnb_complete["neighbourhood_group"]==neighbourhood_group_name].groupby("neighbourhood").count()["id"])
        json_info = self._get_info_from_json(neighbourhood_group_name)

        fig = px.choropleth_mapbox(neighbourhood_in_group, geojson=self.geojson_airbnb,
                                color_continuous_scale = "OrRd",
                                locations="neighbourhood", featureidkey="properties.neighbourhood",
                                center={"lat": json_info["lat"], "lon": json_info["lon"]},
                                hover_data = ["Number of Airbnbs"],
                                mapbox_style="carto-positron", zoom=json_info["zoom"],
                                color = feature,
                                title="Mean Airbnb {} per Neighbourhood".format(feature))
        fig.update_layout(font_family="Sans-serif",)
        
        fig.show()

    def _pie_by_group_visualization_code(self,group):
        to_pie = self.Airbnb_complete[self.Airbnb_complete["neighbourhood_group"] == group].groupby(["room_type"]).count()[["id"]].reset_index()
        go_pie = go.Pie(labels=to_pie["room_type"], values=to_pie["id"],
                name=group,
                hole=0.4,
                #text = acro,
                textinfo='percent+label',

        )
        fig = go.Figure(
            data = go_pie
        )
        fig.update_layout(annotations=[
                dict(text=go_pie.name, showarrow=False,font_size=20)],
                font_family="Sans-serif",)

        fig.update_traces(marker=dict(colors=px.colors.sequential.RdBu,
                                line=dict(color='#FFFFFF', width=5)))
        fig.show()

    # Public

    def map_vizualization(self,group,feature):
        
        neighbourhood_in_group = self.Airbnb_complete[self.Airbnb_complete["neighbourhood_group"]==group].groupby("neighbourhood").mean().reset_index()
        neighbourhood_in_group["Number of Airbnbs"]=list(self.Airbnb_complete[self.Airbnb_complete["neighbourhood_group"]==group].groupby("neighbourhood").count()["id"])
        json_info = self._get_info_from_json(group)

        fig0 = px.choropleth_mapbox(neighbourhood_in_group, geojson=self.geojson_airbnb,
                                color_continuous_scale = "OrRd",
                                locations="neighbourhood", featureidkey="properties.neighbourhood",
                                center={"lat": json_info["lat"], "lon": json_info["lon"]},
                                hover_data = ["Number of Airbnbs"],
                                mapbox_style="carto-positron", zoom=json_info["zoom"],
                                color = feature,
                                title="Mean Airbnb {} per Neighbourhood".format(feature)
                                )
        fig0.update_layout(font_family="Sans-serif",)
        return fig0
        
    def pie_vizualization(self,group,feature):
        
        neighbourhood_in_group = self.Airbnb_complete[self.Airbnb_complete["neighbourhood_group"]==group].groupby("neighbourhood").mean().reset_index()
        neighbourhood_in_group["Number of Airbnbs"]=list(self.Airbnb_complete[self.Airbnb_complete["neighbourhood_group"]==group].groupby("neighbourhood").count()["id"])
        json_info = self._get_info_from_json(group)
        
        # Pie
        to_pie = self.Airbnb_complete[self.Airbnb_complete["neighbourhood_group"] == group].groupby(["room_type"]).count()[["id"]].reset_index()
        go_pie = go.Pie(labels=to_pie["room_type"], values=to_pie["id"],
                name=group,
                hole=0.4,
                #text = acro,
                textinfo='percent+label',

        )
        fig1 = go.Figure(
            data = go_pie
        )
        fig1.update_layout(annotations=[
            dict(text=go_pie.name, showarrow=False,font_size=20-int(len(go_pie.name)/2))]
        )
        fig1.update_traces(marker=dict(colors=px.colors.sequential.RdBu,
                                line=dict(color='#FFFFFF', width=5)))
        fig1.update_layout(title_text="Room Types in {}".format(group),
                    font_family="Sans-serif",)
        return fig1

      
 
    def hist_vizualization(self,group,feature):
        
        neighbourhood_in_group = self.Airbnb_complete[self.Airbnb_complete["neighbourhood_group"]==group].groupby("neighbourhood").mean().reset_index()
        neighbourhood_in_group["Number of Airbnbs"]=list(self.Airbnb_complete[self.Airbnb_complete["neighbourhood_group"]==group].groupby("neighbourhood").count()["id"])
        json_info = self._get_info_from_json(group)

        # Hist
        info = self.Airbnb_complete[self.Airbnb_complete["neighbourhood_group"] == group].groupby(["room_type"]).mean().reset_index()
        info_filtered = info[["room_type","bathrooms","beds","accommodates"]]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=info_filtered["room_type"],
            y=info_filtered["bathrooms"],
            name='Number of bathrooms',
            marker_color=px.colors.sequential.Oranges[2]
        ))
        fig2.add_trace(go.Bar(
            x=info_filtered["room_type"],
            y=info_filtered["beds"],
            name='Number of beds',
            marker_color=px.colors.sequential.Oranges[4]
        ))
        fig2.add_trace(go.Bar(
            x=info_filtered["room_type"],
            y=info_filtered["accommodates"],
            name='How many people can accommodate',
            marker_color=px.colors.sequential.Oranges[6]
        ))
        large_rockwell_template = dict(
                layout=go.Layout(title_font=dict(family="Rockwell", size=24))
        )
        fig2.update_layout(barmode='group', 
            title_text="Mean beds, bathrooms and accommodates per Room Types in {}".format(group),
            template = large_rockwell_template,
            font_family="Sans-serif",
            title_font_family="Sans-serif",
            title_font_size=18,
            )
        return fig2
 


    

    def main_visualization_map(self,feature,detailed=False):

        if detailed:
            to_plot_data = self.main_visualization_detailed
        else:
            to_plot_data = self.main_visualization
            hover_data={'neighbourhood':False,                         
            'neighbourhood_group':True, 
            feature:':.2f', 
            }

        fig = px.choropleth_mapbox(to_plot_data, geojson=self.geojson_airbnb,
                                color=feature,
                                locations="neighbourhood", featureidkey="properties.neighbourhood",
                                center={"lat": self.porto_view_lat, "lon": self.porto_view_lon},
                                mapbox_style="carto-positron", zoom=self.porto_view_zoom,
                                #hover_data=hover_data,
                                color_continuous_scale = "OrRd",
                                #title="Mean {} by neighbourhood group".format(feature.replace("_"," ").capitalize())
                                )
        fig.update_layout(
            height = 900,
            font_family="Sans-serif",
        
        )
        return fig 

    def main_visualization_list(self,feature,detailed=False):
       
        if detailed:
            sorted_list = self.Airbnb_complete.groupby("neighbourhood").mean()[feature].sort_values(ascending=True)
        else:
            sorted_list = self.main_visualization.groupby("neighbourhood_group").mean()[feature].sort_values(ascending=True)
        to_plot =  np.array(list(zip(sorted_list.index,sorted_list)))
        fig = go.Figure(go.Bar(
            y=to_plot[:,0],
            x=np.round(to_plot[:,1].astype(float),decimals=2),
            orientation='h',
             marker=dict(
                color=np.round(to_plot[:,1].astype(float),decimals=2),
                colorscale="OrRd",
            ),
           
        ))
        fig.update_layout(font_family="Sans-serif",
                        )
        return fig

    def bar_room_type_visualization(self,group,feature):
        large_rockwell_template = dict(layout=go.Layout(title_font=dict(family="Rockwell", size=24)))
        to_pie = self.Airbnb_complete[self.Airbnb_complete["neighbourhood_group"] == group].groupby(["room_type"]).mean().reset_index()

        fig = go.Figure(
                    data=[go.Bar(
                        x=to_pie['room_type'], 
                        y=to_pie[feature],
                        text=np.round(to_pie[feature]),
                        textposition='auto',
                        textfont=dict(
                            size=18,
                            family="Sans-serif",
                        ),

                    )]
                )
        # Customize aspect
        fig.update_traces(marker_color='rgb(233,84,32)', marker_line_color='rgb(255,0,0)',
                        marker_line_width=3, opacity=0.7)
        fig.update_layout(title_text='Room Type mean {} in {}'.format(feature.replace("_"," ").capitalize(),group),
                        template = large_rockwell_template,
                        title_font_family="Sans-serif",
                        )
        return fig
    
    def time_series_individual(self,neighbourhood,feature,group):
        to_plot = self.calendar[self.calendar["neighbourhood"] == neighbourhood]
        to_plot_group = self.calendar.groupby(["neighbourhood_group","yearmonth"]).mean().reset_index()
        to_plot_group = to_plot_group[to_plot_group["neighbourhood_group"]==group]
        large_rockwell_template = dict(
                layout=go.Layout(title_font=dict(family="Rockwell", size=24))
            )

        fig = go.Figure([go.Scatter(x=to_plot['yearmonth'], 
                                    y=to_plot[feature],
                                    marker_color="orange",
                                    name = neighbourhood
                                ),
                        go.Scatter(x=to_plot_group['yearmonth'], 
                                    y=to_plot_group[feature],
                                    marker_color="red",
                                    name=group
                                ), 
                                ])
        fig.update_layout(title="{} - {} Mean Analysis".format(neighbourhood,feature.capitalize()),
                        template=large_rockwell_template,
                        title_font_family="Sans-serif")
        
        return fig
    
    '''
    def group_visualization_map(self,neighbourhood_group_name,feature):
        self._group_visualization_map_code(neighbourhood_group_name,feature)

    def pie_by_group_visualization(self,group):
        self._pie_by_group_visualization_code(group)


    def map_pie_hist_vizualization(self,group,feature):
        self._map_pie_hist_vizualization_code(group,feature)
    '''