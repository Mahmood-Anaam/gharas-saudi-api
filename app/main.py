"""
app/main.py
-----------
FastAPI entry-point with two endpoints:
  • GET  /health      → simple heartbeat
  • POST /recommend   → list of suitable plants
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import RecommendationRequest, RecommendationResponse
from .recommender import recommend

app = FastAPI(title="gharas-saudi-api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendationResponse)
async def recommend_endpoint(req: RecommendationRequest):
    try:
        return await recommend(req)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
