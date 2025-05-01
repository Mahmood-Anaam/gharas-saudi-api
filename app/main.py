"""
app/main.py
-----------
FastAPI entry-point with two endpoints:
  • GET  /health      → simple heartbeat
  • POST /recommend   → list of suitable plants
"""

from io import BytesIO
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from .models import RecommendationRequest, RecommendationResponse
from .recommender import recommend
from .generate_image import *
from PIL import Image
from io import BytesIO
import base64


app = FastAPI(title="gharas-saudi-api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

@app.get("/health")
async def health():
    return {"status": "ok"}



@app.post("/generate-plant-image")
async def generate_plant_image(plant_name: str):
    try:
        prompt = plant_image_prompt.format(plant_name=plant_name)
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                # image_data = resize_image(image_data)
                return JSONResponse(content={
                    "status": "success",
                    "image": f"data:image/png;base64,{base64.b64encode(image_data).decode('utf-8')}"
                })

        raise HTTPException(status_code=500, detail="No image generated")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ................................................


@app.post("/recommend", response_model=RecommendationResponse)
async def recommend_endpoint(req: RecommendationRequest):
    try:
        return await recommend(req)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
