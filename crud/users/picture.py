from fastapi import HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from database.connection import db_dependency
from database.models import Users
from schemas.user import UserOutSchema
from file_system.settings import BASE_DIR, IMAGES_USERS_DIR, ALLOWED_CONTENT_TYPE, DEFAULT_PROFILE_PIC
from file_system.methods import compress_image, resize_image
from time import time
from shutil import rmtree
from os import listdir
from errors.my_errors import FILE_IS_NOT_AN_IMAGE, IMAGE_TYPE_NOT_ALLOWED

async def upload_profile_pic(
        id_user: int, 
        picture: UploadFile,
        db: db_dependency
):
    try:
        if picture.content_type in ALLOWED_CONTENT_TYPE:
            rmtree(f"{IMAGES_USERS_DIR}/{id_user}")
            IMAGES_USERS_DIR.joinpath(str(id_user)).mkdir()
            picture.filename = f"{time()}_{id_user}.{picture.content_type.split('/')[1]}"
            dest_path = f"{IMAGES_USERS_DIR}/{id_user}/{picture.filename}"
            with open(dest_path, 'wb+') as dest:
                dest.write(picture.file.read())

            await resize_image(dest_path)

            new_path = ""
            for node in dest_path.split('/')[-4:]:
                new_path += f"/{node}"
            
            user = db.query(Users).filter(Users.id_user==id_user).first()
            user.picture = new_path

            db.commit()
            db.refresh(user)

            return UserOutSchema.model_validate(user)
        else: 
            raise IMAGE_TYPE_NOT_ALLOWED
    except:
        raise FILE_IS_NOT_AN_IMAGE


async def get_profile_pic(
        id_user: int,
        db: db_dependency
):
    try:
        dir = f"{IMAGES_USERS_DIR}/{id_user}/"
        content = listdir(dir)
        if len(content) == 0:
            return {"profile_pic": FileResponse(DEFAULT_PROFILE_PIC), "other_pic": FileResponse(f"{IMAGES_USERS_DIR}/antarctica3.jpg")}
        
        full_path = f"{dir}{content[0]}"
        return {'profile_pic': FileResponse(full_path)}
    except:
        ...


async def delete_profile_pic(
        id_user: int,
        db: db_dependency
):
    rmtree(f"{IMAGES_USERS_DIR}/{id_user}")
    IMAGES_USERS_DIR.joinpath(str(id_user)).mkdir()

    user = db.query(Users).filter(Users.id_user==id_user).first()
    user.picture = DEFAULT_PROFILE_PIC

    db.commit()
    db.refresh(user)
    
    return UserOutSchema.model_validate(user)