import json
import math
import os
import random
import time
from datetime import datetime
from math import asin, cos, radians, sin, sqrt

import gmaps
import gmaps.datasets
import googlemaps
import numpy as np
import pandas as pd
import requests


class ConvenienceEvaluation():
    # fields_to_types
    search_fields = {
        "food": ["restaurant", "cafe"],
        "live": ["convenience_store", "supermarket"],
        "transportation": ["bus_station", "subway_station"],
        "entertainment": ["movie_theater", "gym"],
        "environment": ["park", "school"]
    }

    def __init__(self, address, key):
        # define instance attributes
        self.gmap_client = googlemaps.Client(key=key)
        payload = {"address": address, "key": key}
        re = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json", params=payload)
        self.place_info = json.loads(re.text)
        self.latitude = self.place_info['results'][0]['geometry']['location']['lat']
        self.longitude = self.place_info['results'][0]['geometry']['location']['lng']
        self.places_table = pd.DataFrame()

    def dist_calculator(self, place_lat, place_lon):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # lat:latitude
        # lon:longitude
        # convert decimal degrees to radians
        here_lat = self.latitude
        here_lon = self.longitude
        here_lat, here_lon, place_lat, place_lon = map(
            radians, [here_lat, here_lon, place_lat, place_lon])
        # haversine formula
        diff_lat = place_lat - here_lat
        diff_lon = place_lon - here_lon
        # central angle
        angle = 2 * asin(sqrt(sin(diff_lat/2)**2 + cos(here_lon)
                              * cos(place_lon) * sin(diff_lon/2)**2))
        # radius of earth in kilometers is 6371
        res = 6371 * angle * 1000
        res = round(res, 3)
        return res

    def type_mapping(self, fields):
        self.search_types = []
        for field in fields:
            if field in self.search_fields:
                self.search_types += self.search_fields[field]

    def search(self, radius):
        # https://developers.google.com/places/web-service/search
        """
        key — Your application's API key. This key identifies your application. See Get a key for more information.
        location — The latitude/longitude around which to retrieve place information. This must be specified as latitude,longitude.
        radius — Defines the distance (in meters) within which to return place results.
        The maximum allowed radius is 50 000 meters. Note that radius must not be included if rankby=distance 
        (described under Optional parameters below) is specified.
        """
        position = f'{self.latitude},{self.longitude}'
        places_result = []
        for each_type in self.search_types:
            places_info = self.gmap_client.places_nearby(
                location=position, radius=radius, type=each_type)
            places_result += places_info["results"]
            count = 0
            while (count < 10 and places_info.get("next_page_token")):
                time.sleep(2)
                places_info = self.gmap_client.places_nearby(
                    page_token=places_info["next_page_token"])
                places_result += places_info["results"]
        self.places_table = pd.DataFrame(places_result)
        geo_locate = self.places_table["geometry"].apply(
            lambda x: x["location"])
        self.places_table["distance"] = geo_locate.apply(
            lambda x: self.dist_calculator(x["lat"], x["lng"]))
        self.places_table["distance"].loc[self.places_table["distance"] < 1] = 1
        self.places_table["latitude"] = geo_locate.apply(lambda x: x["lat"])
        self.places_table["longitude"] = geo_locate.apply(lambda x: x["lng"])
        self.places_table["rating"] = self.places_table["rating"].fillna(0)
        self.places_table.sort_values(by=['distance'], inplace=True)

    def get_point(self, grading_manual):
        self.points = {}
        for each_type in grading_manual:
            each_type_count = sum(
                self.places_table["types"].apply(lambda x: each_type in x))
            # inverse distance Weighting for restaurant/cafe
            if each_type in ["restaurant", "cafe"] and bool(grading_manual[each_type]) == 0:
                grading_manual[each_type] = 'self.places_table["rating"] / self.places_table["distance"] ** 0.5'
            each_type_point = round(sum(self.places_table["types"].apply(
                lambda x: each_type in x) * eval(grading_manual[each_type])), 2)
            each_type_point = each_type_point if each_type_point <= 10 else 10
            self.points[each_type] = {
                "count": each_type_count, "point": each_type_point}
        self.points = pd.DataFrame.from_dict(self.points).T
        self.total = round(sum(self.points["point"]), 2)
