from fastapi import HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from database.connection import db_dependency
from database.models import Users, ProjectsUsers, Projects
from schemas.user import UserOutSchema
from schemas.project import ProjectOutSchema
from time import time
from file_system.settings import BASE_DIR, IMAGES_USERS_DIR, ALLOWED_CONTENT_TYPE, DEFAULT_PROFILE_PIC, IMAGES_PROJECTS_DIR
from file_system.methods import compress_image
from shutil import rmtree
from os import listdir
from file_system.settings import DEFAULT_PROJECT_PIC
from errors.my_errors import FILE_IS_NOT_AN_IMAGE, IMAGE_TYPE_NOT_ALLOWED, PERMISSION_DENIED_ERROR


async def upload_project_pic(
       id_user: int,
       id_project: int,
       picture: UploadFile,
       db: db_dependency 
):  
    user = db.query(ProjectsUsers).filter(ProjectsUsers.id_project==id_project, ProjectsUsers.id_user==id_user).first()
    if user:
        if user.role != "owner":
            raise PERMISSION_DENIED_ERROR
    else:
            raise PERMISSION_DENIED_ERROR
    del user

    if picture.content_type in ALLOWED_CONTENT_TYPE:
        rmtree(f"{IMAGES_PROJECTS_DIR}/{id_project}/logo")
        IMAGES_PROJECTS_DIR.joinpath(str(id_project)).joinpath("logo").mkdir()
        picture.filename = f"{time()}_{id_project}.{picture.content_type.split('/')[1]}"
        dest_path = f"{IMAGES_PROJECTS_DIR}/{id_project}/logo/{picture.filename}"
        with open(dest_path, 'wb+') as dest:
            dest.write(picture.file.read())

        await compress_image(dest_path)

        new_path = ""
        for node in dest_path.split('/')[-5:]:
            new_path += f"/{node}"
            
        project = db.query(Projects).filter(Projects.id_project==id_project).first()
        project.picture = new_path

        db.commit()
        db.refresh(project)

        return ProjectOutSchema.model_validate(project)
    else: 
        raise IMAGE_TYPE_NOT_ALLOWED


async def delete_project_pic(
    id_user: int,
    id_project: int,
    db: db_dependency 
):
    user = db.query(ProjectsUsers).filter(ProjectsUsers.id_project==id_project, ProjectsUsers.id_user==id_user).first()
    if user:
        if user.role != "owner":
            raise PERMISSION_DENIED_ERROR
    else:
            raise PERMISSION_DENIED_ERROR
    del user

    rmtree(f"{IMAGES_PROJECTS_DIR}/{id_project}/logo")
    IMAGES_PROJECTS_DIR.joinpath(str(id_project)).joinpath("logo").mkdir()

    project = db.query(Projects).filter(Projects.id_project==id_project).first()
    project.picture = DEFAULT_PROJECT_PIC

    db.commit()
    db.refresh(project)
    
    return ProjectOutSchema.model_validate(project)