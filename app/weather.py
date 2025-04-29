"""
app/weather.py
--------------
Current weather helper (free tier) via:
https://api.openweathermap.org/data/2.5/weather
"""

from __future__ import annotations

import os
from typing import Tuple

import httpx

OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_API_KEY")
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"

if not OPEN_WEATHER_KEY:
    raise RuntimeError("OPEN_WEATHER_API_KEY missing in environment")


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
