"""Openmeteo weather model."""

import datetime

import openmeteo_requests  # type: ignore
import pandas as pd
import pytz
import requests
from openmeteo_requests.Client import OpenMeteoRequestsError  # type: ignore

from ...cache import MEMORY
from ..weather_model import WeatherModel


@MEMORY.cache(ignore=["session"])
def create_openmeteo_weather_model(
    session: requests.Session,
    latitude: float,
    longitude: float,
    dt: datetime.datetime,
    tz: str,
) -> WeatherModel:
    """Create a weather model from openmeteo."""
    # pylint: disable=broad-exception-caught
    client = openmeteo_requests.Client(session=session)
    temperature = None
    try:
        responses = client.weather_api(
            "https://historical-forecast-api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "start_date": str((dt - datetime.timedelta(days=1.0)).date()),
                "end_date": str(dt.date()),
                "hourly": [
                    "temperature_2m",
                    "relative_humidity_2m",
                    "dew_point_2m",
                    "apparent_temperature",
                    "precipitation",
                    "rain",
                    "snowfall",
                    "snow_depth",
                    "weather_code",
                    "pressure_msl",
                    "surface_pressure",
                    "cloud_cover",
                    "cloud_cover_low",
                    "cloud_cover_mid",
                    "cloud_cover_high",
                    "et0_fao_evapotranspiration",
                    "vapour_pressure_deficit",
                    "wind_speed_10m",
                    "wind_speed_100m",
                    "wind_direction_10m",
                    "wind_direction_100m",
                    "wind_gusts_10m",
                    "soil_temperature_0_to_7cm",
                    "soil_temperature_7_to_28cm",
                    "soil_temperature_28_to_100cm",
                    "soil_temperature_100_to_255cm",
                    "soil_moisture_0_to_7cm",
                    "soil_moisture_7_to_28cm",
                    "soil_moisture_28_to_100cm",
                    "soil_moisture_100_to_255cm",
                ],
                "daily": [
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "temperature_2m_mean",
                    "apparent_temperature_max",
                    "apparent_temperature_min",
                    "apparent_temperature_mean",
                    "sunrise",
                    "sunset",
                    "daylight_duration",
                    "sunshine_duration",
                    "precipitation_sum",
                    "rain_sum",
                    "snowfall_sum",
                    "precipitation_hours",
                    "wind_speed_10m_max",
                    "wind_gusts_10m_max",
                    "wind_direction_10m_dominant",
                    "shortwave_radiation_sum",
                    "et0_fao_evapotranspiration",
                ],
                "timezone": tz,
            },
        )
    except (requests.exceptions.RetryError, OpenMeteoRequestsError):
        temperature = None
        return WeatherModel(temperature=temperature)
    except Exception as e:
        e_text = str(e)
        if "Parameter 'start_date' is out of allowed range from" in e_text:
            temperature = None
            return WeatherModel(temperature=temperature)
        raise e
    if not responses:
        temperature = None
        return WeatherModel(temperature=temperature)
    response = responses[0]
    try:
        hourly = response.Hourly()
    except Exception:
        # print(f"Encountered problem unpacking weather: {e}, skipping")
        temperature = None
        return WeatherModel(temperature=temperature)
    if hourly is None:
        raise ValueError("hourly is null.")
    hourly_df = pd.DataFrame(
        index=pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s"),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
            tz=tz,
        )[: len(hourly.Variables(0).ValuesAsNumpy())],  # type: ignore
        data={
            "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),  # type: ignore
        },
    )
    dt = dt.replace(tzinfo=None)
    timezone = pytz.timezone(tz)
    dt = timezone.localize(dt)
    hourly_idx = hourly_df.index.get_indexer([dt], method="nearest")[0]
    temperature = hourly_df.iloc[hourly_idx]["temperature_2m"]  # type: ignore
    return WeatherModel(temperature=temperature)
