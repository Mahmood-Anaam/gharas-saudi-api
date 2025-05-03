from __future__ import annotations
import json
from pathlib import Path
from typing import List
import numpy as np
from .models import Plant, ClimateCategory, PlantType, SoilType

# ---------- Level map: ClimateCategory -> int 0-4 ----------
_LEVEL = {
    "Very Low": 0,
    "Low": 1,
    "Moderate": 2,
    "High": 3,
    "Extreme": 4,
}

# ---------- Vector encoders ----------
def plant_vector(plant: Plant) -> list[float]:
    """Return [temp_lvl, hum_lvl, precip_lvl] for one plant."""
    return [
        _LEVEL[plant.temperature[0].value],
        _LEVEL[plant.humidity[0].value],
    ]


def site_vector(mean_T: float, mean_H: float) -> list[float]:
    """Map numeric climate means into the same 0-4 space."""
    temp_lvl = np.clip(np.interp(mean_T, [-10, 12, 24, 34, 42], [0, 1, 2, 3, 4]), 0, 4)
    hum_lvl  = np.clip(np.interp(mean_H, [0, 25, 40, 60, 80],  [0, 1, 2, 3, 4]), 0, 4)
    return [temp_lvl, hum_lvl]


# ---------- Dataset loader ----------
def load_plants(json_path: Path) -> List[Plant]:
    """Read plants_dataset.json and convert records to Plant objects."""
    with json_path.open(encoding="utf-8") as f:
        records = json.load(f)

    plants: list[Plant] = []
    for rec in records:
        plants.append(
            Plant(
                name=rec["name"],
                type=PlantType(rec["type"]),
                temperature=[ClimateCategory(cat) for cat in rec["temperature"]],
                humidity=[ClimateCategory(cat) for cat in rec["humidity"]],
                soil=[SoilType(cat) for cat in rec["soil"]],
            )
        )
    return plants
