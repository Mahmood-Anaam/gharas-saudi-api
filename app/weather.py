"""
app/weather.py
--------------
OpenWeather One-Call time-machine helper.
"""

from __future__ import annotations

import datetime as dt
import os
from typing import Tuple, Optional

import httpx

OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_API_KEY")
ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall/timemachine"

if not OPEN_WEATHER_KEY:
    raise RuntimeError("OPEN_WEATHER_API_KEY missing in environment")


async def _daily_means(lat: float, lon: float, day: dt.date) -> Tuple[float, float, float]:
    """Fetch one day’s hourly data → (mean_T °C, mean_H %, sum_precip mm)."""
    unix_noon = int(dt.datetime.combine(day, dt.time(12)).timestamp())
    params = {
        "lat": lat,
        "lon": lon,
        "dt": unix_noon,
        "units": "metric",
        "appid": OPEN_WEATHER_KEY,
    }
    async with httpx.AsyncClient(timeout=15) as client:
        res = await client.get(ONECALL_URL, params=params)
        res.raise_for_status()
        data = res.json()

    hourly = data.get("hourly", [])
    temps = [h["temp"] for h in hourly]
    hums  = [h["humidity"] for h in hourly]
    precs = [
        h.get("rain", {}).get("1h", 0.0) + h.get("snow", {}).get("1h", 0.0)
        for h in hourly
    ]
    return sum(temps) / len(temps), sum(hums) / len(hums), sum(precs)


async def fetch_monthly_means(
    lat: float,
    lon: float,
    month: Optional[int] = None,
) -> Tuple[float, float, float]:
    """
    Return (mean_T °C, mean_H %, mean_precip mm/day) for last 30 days or a calendar month.
    """
    today = dt.date.today()

    if month is None:
        end_date = today
        start_date = end_date - dt.timedelta(days=29)
    else:
        year = today.year
        start_date = dt.date(year, month, 1)
        end_date = (start_date.replace(day=28) + dt.timedelta(days=4)).replace(day=1) - dt.timedelta(days=1)

    tot_T = tot_H = tot_P = 0.0
    days = 0
    delta_days = (end_date - start_date).days + 1

    for d in range(delta_days):
        day = start_date + dt.timedelta(days=d)
        try:
            t, h, p = await _daily_means(lat, lon, day)
        except Exception:
            continue
        tot_T += t
        tot_H += h
        tot_P += p
        days += 1

    if days == 0:
        raise ValueError("Weather API returned no usable data")

    return tot_T / days, tot_H / days, tot_P / days
