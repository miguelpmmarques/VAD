
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



class DatasetAirbnb:
    def __init__(self, path_to_folder):
        self.path_to_folder = path_to_folder
        self.data_files = {}
        self.Airbnb_complete = None
        self.Airbnb_dropna = None
        self.calendar = None

    # Private
    def _importCsv(self,file_name):
        self.data_files[file_name] = pd.read_csv(self.path_to_folder+"/"+file_name)

    def _importJson(self,file_name):
        with open(self.path_to_folder+"/"+file_name, 'r') as f:
            data=f.read()
        self.data_files[file_name] = json.loads(data)
        
    def _importGeoJson(self,file_name):
        with open(self.path_to_folder+"/"+file_name) as f:
            self.data_files[file_name] = geojson.load(f)
        
    def _calendarPreprocessing(self):
        self.calendar.date = list(map(lambda x: datetime.strptime(x, "%Y-%m-%d"),self.calendar.date))
        self.calendar.price = list(map(lambda x: float(x[1:].replace(',', '') ), self.calendar.price))
        self.calendar.adjusted_price = list(map(lambda x: float(x[1:].replace(',', '') ), self.calendar.adjusted_price))
        self.calendar["yearmonth"] =  self.calendar.date.dt.to_period("M").astype(str)
        self.calendar = self.calendar.join(self.Airbnb_complete[["id","neighbourhood_group","neighbourhood","latitude","longitude"]].set_index('id'), on='listing_id')
        self.calendar.to_csv(self.path_to_folder+"/"+'calendar_final.csv', index=False,index_label=False)
    
    def _bathrooms(self,df):
        translater = {
            '0 shared baths':0,
            '0 baths':0,
            'Shared half-bath':0.5,
            'Private half-bath':0.5,
            'Half-bath':0.5,
            '1 bath':1,
            '1 private bath':1,
            '1 shared bath':1,
            '1.5 shared baths':1.5,
            '1.5 baths':1.5,
            '2 baths':2,
            '2.5 baths':2.5,
            '2 shared baths':2,
            '2.5 shared baths':2.5,
            '3 baths':3,
            '3 shared baths':3,
            '3.5 shared baths':3.5,
            '3.5 baths':3.5,
            '4 baths':4,
            '4 shared baths':4,
            '4.5 shared baths':4.5,
            '4.5 baths':4.5,
            '5 baths':5,
            '5 shared baths':5,
            '5.5 baths':5.5,
            '6 baths':6,
            '6.5 baths':6.5,
            '6.5 shared baths':6.5,
            '7 baths':7,
            '7.5 baths':7.5,
            '8 baths':8,
            '8.5 baths':8.5,
            '9 baths':9,
            '9 shared baths':9,
            '9.5 baths':9.5,
            '10 baths':10,
            '16 baths':16,
            np.nan:0
        }
        return df['bathrooms_text'].replace(translater)


    def _preprocessingData(self):

        listings = self.data_files["listings.csv"]
        listings_summary = self.data_files["listings_summary.csv"]
        listings_summary['bathrooms'] = self._bathrooms(listings[["bathrooms_text"]])
        final_dataset = listings_summary.join(listings[["id","property_type","beds","host_listings_count","instant_bookable","first_review","accommodates","review_scores_rating"]].set_index('id'),on="id")
        final_dataset = final_dataset.drop(columns=["host_name","name","host_id"])
        final_dataset["beds"] = final_dataset["beds"].fillna(0)
        final_dataset["reviews_per_month"] = final_dataset["reviews_per_month"].fillna(0)
        final_dataset["host_listings_count"] = final_dataset["host_listings_count"].fillna(0)
        # Substitui os nans por 1 de janeiro de 2020
        final_dataset_drop_na = final_dataset.copy()
        final_dataset_drop_na = final_dataset_drop_na.dropna()

        # Replace nan values
        final_dataset["first_review"] = list(map(lambda x: datetime.strptime(x, "%Y-%m-%d"),final_dataset["first_review"].fillna("2020-1-1")))
        final_dataset["last_review"] = list(map(lambda x: datetime.strptime(x, "%Y-%m-%d"),final_dataset["last_review"].fillna("2020-1-1")))
        
        # Save to csv
        final_dataset_drop_na.to_csv(self.path_to_folder+"/"+'Airbnb_drop_na.csv', index=False,index_label=False)
        final_dataset.to_csv(self.path_to_folder+"/"+'Airbnb_complete.csv', index=False,index_label=False)
        self.Airbnb_complete = final_dataset
        self.Airbnb_dropna = final_dataset_drop_na

    # Public
    def importData(self,calendar = True):
        files = os.listdir(self.path_to_folder)
        
        if 'Airbnb_complete.csv' in files and 'Airbnb_drop_na.csv' in files:
            
            self.Airbnb_complete = pd.read_csv(self.path_to_folder+"/"+"Airbnb_complete.csv")
            self.Airbnb_dropna = pd.read_csv(self.path_to_folder+"/"+"Airbnb_drop_na.csv")
            print("Data already preprocessed")
            if calendar:
                if "calendar_final.csv" in files:
                    self.calendar = pd.read_csv(self.path_to_folder+"/"+"calendar_final.csv")
                else:
                    self.calendar = pd.read_csv(self.path_to_folder+"/"+"calendar.csv")
                    print("Preparing Calendar")
                    self._calendarPreprocessing()
            self._importGeoJson("neighbourhoods.geojson")
            self._importJson("neighbourhood_group_list.json")

            return
        
        print("Uploading and Cleaning Data...\nProbably gonna take a while")
        for f in files:
            codec = f.split(".")[-1]
            if codec == "csv":
                self._importCsv(f)
            elif codec == "geojson":
                self._importGeoJson(f)
            elif codec == "json":
                self._importJson(f)
            else:
                print("Not ready to read that codec yet :)")
        self._preprocessingData()
        if calendar:
            if "calendar_final.csv" in files:
                self.calendar = self.data_files["calendar_final.csv"]
            else:
                self.calendar = self.data_files["calendar.csv"]
                self._calendarPreprocessing()
