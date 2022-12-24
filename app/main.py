import os
from typing import Union

import aiofiles
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import asyncio
from PIL import Image

from app.lib.utils import create_image, image_variation
CHUNK_SIZE = 4096 * 4096

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "Welcome to DALL.E"}


@app.get("/heartbeat")
async def heartbeat():
    return JSONResponse(
        status_code=200,
        content={"message": "alive"},
    )


@app.get("/generate-image/")
async def generate_image(text: str):
    # dalle_image = create_image(text)
    await asyncio.sleep(5)
    dalle_image = "https://via.placeholder.com/1024"
    return dalle_image


async def upload_and_generate_image(request: Request, file: UploadFile, count: int = 1):
    form = await request.form()
    filename = file.filename
    file_mask = ["png"]
    file_ext = filename.rsplit(".", 1)[1]
    filename_without_ext = filename.rsplit(".", 1)[0]

    try:
        if not os.path.exists('./upload'):
            os.makedirs('upload')

        async with aiofiles.open(f'upload/{file.filename}', 'wb') as out_file:
            print("Starting file upload")
            content = await file.read(CHUNK_SIZE)
            while content:  # async read chunk
                await out_file.write(content)  # async write chunk
                content = await file.read(CHUNK_SIZE)

        if file_ext not in file_mask:
            im = Image.open(f'upload/{file.filename}')
            width, height = im.size
            if width > 1024 and height > 1024:
                size = 1024
            else:
                size = min(width, height)
            im = im.resize((size, size))
            im.save(f'upload/{filename_without_ext}.png')

        print("File upload done. starting Image Processing with DALLE.")
        dalle_variation_image = image_variation(f'upload/{filename_without_ext}.png', count)

        return dalle_variation_image
    except Exception as e:
        print(e)


@app.post("/generate-variation/{count}")
async def generate_image_variation(count: int, request: Request, file: UploadFile):
    try:
        dalle_variation_image = await upload_and_generate_image(request, file, count)
        return JSONResponse(
            status_code=200,
            content={"message": "Variation Image Generated", "images": dalle_variation_image},
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"message": f"Oops! Something went wrong..."},
        )
