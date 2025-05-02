from __future__ import annotations
import os
from typing import Tuple
import httpx
from app.models import SoilType, Weather

OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_API_KEY")
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"

if not OPEN_WEATHER_KEY:
    raise RuntimeError("OPEN_WEATHER_API_KEY missing in environment")


async def determine_soil_type(lat: float, lon: float) -> SoilType:
    """
    Determines soil type based on location coordinates.
    This is a simplified version - you should replace with actual soil data.
    """
    # TODO: Replace with actual soil data lookup for Saudi Arabia
    # This is just a placeholder logic
    if 24.5 <= lat <= 25.0 and 46.5 <= lon <= 47.0:  # Approx Riyadh area
        return SoilType.SANDY
    elif 21.0 <= lat <= 24.0 and 39.0 <= lon <= 42.0:  # Approx Western region
        return SoilType.CALCAREOUS
    else:
        return SoilType.SANDY_LOAM  # Default value

async def fetch_weather(lat: float, lon: float):
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "appid": OPEN_WEATHER_KEY,
    }

    try:

        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(CURRENT_URL, params=params)
            res.raise_for_status()
            data = res.json()
        soil_type = await determine_soil_type(lat, lon)
        return Weather(
            temp=data['main']['temp'],
            humidity=data['main']['humidity'],
            region=data['name'],
            soil=soil_type
        )
    except Exception as e:
        print(e)


async def fetch_current_means(lat: float, lon: float) -> Tuple[float, float, float]:
    """
    Return (temp_C, humidity_pct, precip_mm_last_hour) using the free /weather endpoint.
    """
    params = {
        "lat": lat,
        "lon": lon,
        "units": "metric",
        "appid": OPEN_WEATHER_KEY,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.get(CURRENT_URL, params=params)
        res.raise_for_status()
        data = res.json()

    temp_c  = data["main"]["temp"]
    hum_pct = data["main"]["humidity"]

    precip_mm = 0.0
    # rain.1h or snow.1h may be absent
    if "rain" in data and "1h" in data["rain"]:
        precip_mm += data["rain"]["1h"]
    if "snow" in data and "1h" in data["snow"]:
        precip_mm += data["snow"]["1h"]

    return temp_c, hum_pct, precip_mm
