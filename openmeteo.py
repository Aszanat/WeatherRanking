import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

from datetime import date, timedelta
import numpy as np

cities = {
    "Warsaw": (52.2298, 21.0118),
    "Gdansk": (54.3523, 18.6491),
    "Berlin": (52.5244, 13.4105),
    "Krakow": (50.0614, 19.9366),
    "Nurnberg": (49.4542, 11.0775),
    "Munich": (48.1374, 11.5755)
}

def connect_to_openmeteo():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	    "latitude": [place[0] for place in cities.values()],
	    "longitude": [place[1] for place in cities.values()],
	    "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "cloud_cover"],
        "timezone": "auto",
	    "start_date": date.today() - timedelta(days=1),
	    "end_date": date.today() - timedelta(days=1)
    }
    responses = openmeteo.weather_api(url, params=params)

    scores = {}
    cities_list = list(cities.keys())

    for i in range(len(responses)):
        response = responses[i]
        city = cities_list[i]
        print(city)
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
        hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
        hourly_cloud_cover = hourly.Variables(3).ValuesAsNumpy()

        temperature_mean = np.mean(hourly_temperature_2m)
        humidity_mean = np.mean(hourly_relative_humidity_2m)
        wind_speed_mean = np.mean(hourly_wind_speed_10m)
        cloud_cover_mean = np.mean(hourly_cloud_cover)

        temperature_score = np.max([10 - abs(24 -round(temperature_mean)), 0])
        print("Temperature " + str(temperature_mean) + " scores " + str(temperature_score))

        wind_score = np.max([10 - (round(wind_speed_mean / 6)), 0])
        # 6 - arbitrary number inspired by beauffort's scale
        print("Wind speed " + str(wind_speed_mean) + " scores " + str(wind_score))

        humidity_score = 10 - round(abs(50 - humidity_mean)/5)
        print("Humidity " + str(humidity_mean) + " scores " + str(humidity_score))

        cloud_score = 10 - (cloud_cover_mean < 25)*round((25 - cloud_cover_mean)/2.5) - (cloud_cover_mean > 25)*round((cloud_cover_mean - 25)/7.5)
        print("Cloud cover " + str(cloud_cover_mean) + " scores " + str(cloud_score))


