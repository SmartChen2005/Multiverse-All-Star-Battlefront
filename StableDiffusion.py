import openai
import requests
from PIL import Image
from io import BytesIO
import os

# response = openai.images.generate(
#     prompt="A lovely cartoon girl with white hair",
#     n=1,
#     size="256x256"
# )


# image_url = response.data[0].url
# image_data = requests.get(image_url).content
# image = Image.open(BytesIO(image_data))
# image.save(f"{cwd}dalle_painting.png")

def create_and_save_figure(prompt, pic_url):
    response = openai.images.generate(
    prompt=f"An Individual with the following characteristics: {prompt}",
    n=1,
    size="256x256"
    )
    image_url = response.data[0].url
    image_data = requests.get(image_url).content
    image = Image.open(BytesIO(image_data))
    image.save(pic_url)
