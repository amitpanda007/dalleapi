import os

import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_APIKEY = os.getenv('OPENAI_APIKEY')

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