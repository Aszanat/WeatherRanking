import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

from datetime import date, timedelta

def connect_to_openmeteo():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	    "latitude": [52.2298, 54.3523, 52.5244, 50.0614, 49.4542, 48.1374],
	    "longitude": [21.0118, 18.6491, 13.4105, 19.9366, 11.0775, 11.5755],
	    "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "cloud_cover"],
        "timezone": "auto",
	    "start_date": date.today(),#"2025-06-11",
	    "end_date": date.today()#"2025-06-25"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
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

    hourly_data = {"date": pd.date_range(
	    start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	    end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	    freq = pd.Timedelta(seconds = hourly.Interval()),
	    inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["cloud_cover"] = hourly_cloud_cover

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    print(hourly_dataframe)
