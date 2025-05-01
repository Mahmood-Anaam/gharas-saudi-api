from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from google import genai
from google.genai import types
from PIL import Image
import io
import base64
import os



plant_image_prompt = """
Generate a high-quality, photorealistic image of a {plant_name} plant with the following characteristics:
    - Professional studio lighting
    - Isolated on transparent background
    - 4K resolution
    - Detailed textures and accurate colors
    - Perfect for agricultural or gardening app
    """.strip()


plant_simulation_prompt = """
    Create a realistic simulation of a {plant_name} planted in this environment with the following requirements:
        - Seamlessly blend the plant into the environment
        - Match lighting and shadows realistically
        - Maintain natural proportions
        - Output should look like professional gardening simulation
        - Keep the original environment perspective
        """.strip()


def resize_image(image_data: bytes, max_size: tuple = (200, 200)) -> bytes:
    img = Image.open(io.BytesIO(image_data))
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img.save(output, format='PNG', optimize=True, quality=85)
    return output.getvalue()

# def generate_image(prompt: str):
#     try:
#         response = client.models.generate_content(
#             model="gemini-2.0-flash-exp-image-generation",
#             contents=[prompt],
#             config=types.GenerateContentConfig(
#                 response_modalities=['TEXT', 'IMAGE']
#             )
#         )

#         for part in response.candidates[0].content.parts:
#             if part.inline_data is not None:
#                 image_data = part.inline_data.data
#                 return JSONResponse(content={
#                     "status": "success",
#                     "image": f"data:image/png;base64,{base64.b64encode(image_data).decode('utf-8')}"
#                 })

#         raise HTTPException(status_code=500, detail="No image generated")

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/generate-plant-simulation")
# async def generate_plant_simulation(
#     plant_image: UploadFile = File(...),
#     plant_name: str = "cactus",
#     environment_image: UploadFile = File(...),
#     environment_description: str = "garden"
#     ):

  
#     try:
        
#         plant_img = Image.open(io.BytesIO(await plant_image.read()))
#         env_img = Image.open(io.BytesIO(await environment_image.read()))

#         plant_simulation_prompt = (
#             "Create a realistic simulation of a {plant_name} planted in this {environment_description}. "
#             "Requirements:\n"
#             "- Blend the plant naturally into the environment\n"
#             "- Match lighting and shadows accurately\n"
#             "- Maintain proper perspective\n"
#             "- Output should look photorealistic"
#         ).format(plant_name=plant_name, environment_description=environment_description)

    #     response = client.models.generate_content(
    #         model="gemini-2.0-flash-exp-image-generation",
    #         contents=[prompt, plant_img, env_img],
    #         config=types.GenerateContentConfig(
    #             response_modalities=['IMAGE']
    #         )
    #     )

    #     for part in response.candidates[0].content.parts:
    #         if part.inline_data is not None:
    #             image_data = part.inline_data.data
    #             return JSONResponse(content={
    #                 "status": "success",
    #                 "image": f"data:image/png;base64,{base64.b64encode(image_data).decode('utf-8')}"
    #             })

    #     raise HTTPException(status_code=500, detail="No image generated")

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

