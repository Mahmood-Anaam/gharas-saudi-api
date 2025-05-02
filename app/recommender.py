from __future__ import annotations
from pathlib import Path
from typing import List
import numpy as np
from sklearn.neighbors import NearestNeighbors
from .models import (
    Plant,
    RecommendationRequest,
    RecommendationResponse,
)
from .helper import load_plants, plant_vector, site_vector
from .weather import fetch_current_means, fetch_weather  

# ---------- Load dataset ----------
DATA_PATH = Path(__file__).parent / "data" / "plants_dataset.json"
PLANTS: List[Plant] = load_plants(DATA_PATH)

# ---------- Build exact k-NN index ----------
PLANT_MATRIX = np.array([plant_vector(p) for p in PLANTS], dtype="float32")
KNN = NearestNeighbors(
    n_neighbors=min(20, len(PLANTS)),
    metric="euclidean",
).fit(PLANT_MATRIX)


# ---------- Public helper ----------
async def recommend(req: RecommendationRequest) -> RecommendationResponse:
    """Return `limit` nearest plants (climate only)."""
    mean_T, mean_H, mean_P = await fetch_current_means(req.lat, req.lon)
    weather = await fetch_weather(req.lat,req.lon)
    query_vec = np.array([site_vector(mean_T, mean_H, mean_P)], dtype="float32")

    distances, indices = KNN.kneighbors(query_vec, n_neighbors=req.limit)
    recommendations = [PLANTS[i] for i in indices[0]]

    return RecommendationResponse(recommendations=recommendations,weather=weather)
