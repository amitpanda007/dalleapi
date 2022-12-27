import os

import openai
from PIL import Image, ExifTags, ImageOps
from dotenv import load_dotenv

load_dotenv()
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY')
print(OPENAI_APIKEY)

openai.api_key = OPENAI_APIKEY


def create_image(text: str):
    # 256x256, 512x512, or 1024x1024
    response = openai.Image.create(
        prompt=text,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url


def image_variation(image_path: str, count: int = 1):
    try:
        response = openai.Image.create_variation(
            image=open(image_path, "rb"),
            n=count,
            size="1024x1024"
        )
        image_urls = response['data']
        return image_urls
    except Exception as e:
        print(e)


def image_thumbnail(img):
    width, height = img.size
    img = ImageOps.exif_transpose(img)

    if width > 1024 and height > 1024:
        size = 512, 512
    else:
        size = min(width, height), min(width, height)
    print(size)
    image = img.resize(size, Image.Resampling.LANCZOS)
    return image