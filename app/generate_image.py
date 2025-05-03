from PIL import Image
import io




plant_image_prompt = """
Generate a high-quality, photorealistic image of a {plant_name} plant with the following characteristics:
    - Professional studio lighting
    - Isolated on transparent background
    - 4K resolution
    - Detailed textures and accurate colors
    - Perfect for agricultural or gardening app
    """.strip()


plant_simulation_prompt = """
You are an advanced landscape design assistant specializing in simulation rendering.

Your goal is to generate a realistic image that shows what a specific environment would look like if a given plant were added, based on the plant and the environment photos provided.

Inputs:
- Image 1: A high-quality photo of the plant (to be integrated).
- Image 2: A real photo of the user’s environment (where the plant is to be simulated).

Instructions:
- Your primary task is to *insert the plant from Image 1 naturally* into Image 2.
- **Preserve all visual and spatial details** of the environment in Image 2. Do not modify any structure, object, lighting, wall, floor, or perspective.
- **Do not apply any filters or visual effects**.
- Match the lighting, scale, and angle of the environment exactly when placing the plant.

Contextual guidelines based on environment type (infer based on Image 2 if not specified):

1. **Balcony / Terrace**:
   - Place 1 or 2 potted plants along the wall or railing.
   - Do not cover the view or light source.
   - Use medium to large pots and ensure proper shadow casting on the floor.

2. **Garden / Backyard**:
   - Integrate the plant into the soil area near existing vegetation or fence lines.
   - Avoid overlap with existing trees.
   - Maintain open space in the center.

3. **Entrance / Walkway**:
   - Place a symmetrical pair of potted plants on both sides of the door or pathway.
   - Keep alignment straight and elegant.
   - Ensure the plant doesn’t block passage or visual flow.

4. **Indoor Corner / Living Space**:
   - Add one potted plant in the corner where it fits naturally with furniture and light.
   - Use modern ceramic or neutral pots.
   - Align shadows with window lighting.

5. **Roof / Open Floor**:
   - Place the plant near a wall or boundary edge, not in the center.
   - Use large decorative pots or built-in planters.
   - Emphasize clean aesthetics with few repetitions.

Output:
- A single high-resolution simulation image that shows Image 2 with the plant from Image 1 fully integrated and respecting all the above constraints.
        """.strip()


def resize_image(image_data: bytes, max_size: tuple = (300, 300)) -> bytes:
    img = Image.open(io.BytesIO(image_data))
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()


