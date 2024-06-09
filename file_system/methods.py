from PIL import Image
from fastapi import UploadFile
from .settings import IMAGES_USERS_SIZE, PROFILE_PIC_SIZE
import zipfile


async def compress_image(path_to_img: str):
    img = Image.open(path_to_img)
    img.thumbnail(IMAGES_USERS_SIZE)
    img.save(path_to_img)


async def resize_image(path_to_img: str):
    img = Image.open(path_to_img)
    img = img.resize(PROFILE_PIC_SIZE)
    img.save(path_to_img)


async def compress_file(file_path, zip_path, filename):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(filename=file_path, arcname=filename)  

    
async def compress_files(file_paths, zip_path, filenames):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for index, file_path in enumerate(file_paths):
            zipf.write(file_path, filenames[index])