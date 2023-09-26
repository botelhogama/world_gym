import time

import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

import requests

geolocator = Nominatim(user_agent="my-app" , timeout=10)

def geocode_address(address):
    try:
        location = geolocator.geocode(address, timeout=10)
        return location
    except (GeocoderTimedOut, GeocoderUnavailable, ReadTimeoutError):
        return None

def calculate_distance(coord1, coord2):
    if coord1 is None or coord2 is None or coord1 == (None, None) or coord2 == (None, None):
        return np.nan  # if either coordinate is None, return NaN
    else:
        return geodesic(coord1, coord2).kilometers


def calculate_distance_list(addresses1: object, addresses2: object) -> object:
    distances = []

    for i, (coord1, coord2) in enumerate(zip(addresses1, addresses2)):
        try:
            # Check if any coordinate pair is None
            if coord1 is None or coord2 is None:
                distances.append(None)
            else:
                distances.append(geodesic(coord1, coord2).km)
        except ValueError as e:
            print(f"Error at index {i}: {e}")
            distances.append(None)

    return distances

def get_coord(address):
    location = geolocator.geocode(address, timeout=10)
    if location is not None:
        return (location.latitude, location.longitude)
    else:
        return (None, None)


def apply_map(df, column, map_name):
    df[column] = df[column ].str.upper()
    df[column] = df[column].replace(map_name)
    return df


def get_coordinates_from_cep(cep):
    location = geolocator.geocode(cep)
    if location is not None:
        return (location.latitude, location.longitude)
    else:
        return (None, None)


def find_similar_dist(shortzip, data):
    for i in range(7, 3):  # 5, 2, -1
        base_shortzip = shortzip[:i]
        similar_data = data[(data['dist'] <= 150) & (data['dist'].notnull()) & (data['shortzip'].str.startswith(base_shortzip))]

        if not similar_data.empty:
            return similar_data.iloc[0]['dist']
    return


