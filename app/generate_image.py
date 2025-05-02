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
    Create a realistic simulation of a {plant_name} planted in this environment with the following requirements:
        - Seamlessly blend the plant into the environment
        - Match lighting and shadows realistically
        - Maintain natural proportions
        - Output should look like professional gardening simulation
        - Keep the original environment perspective
        """.strip()


def resize_image(image_data: bytes, max_size: tuple = (300, 300)) -> bytes:
    img = Image.open(io.BytesIO(image_data))
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img.save(output, format='PNG')
    return output.getvalue()


