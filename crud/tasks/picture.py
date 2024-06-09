from fastapi import HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from database.connection import db_dependency
from database.models import Users, ProjectsUsers, Projects, Tasks, Subtasks
from schemas.user import UserOutSchema
from schemas.project import ProjectOutSchema
from schemas.task import TaskProjOutSchema
from schemas.subtask import SubtaskOutSchema
from time import time
from file_system.settings import ALLOWED_CONTENT_TYPE, IMAGES_PROJECTS_DIR, DEFAULT_TASK_PIC, BASE_DIR
from file_system.methods import compress_image
from shutil import rmtree
from os import listdir, remove
from file_system.settings import DEFAULT_PROJECT_PIC
from errors.my_errors import FILE_IS_NOT_AN_IMAGE, IMAGE_TYPE_NOT_ALLOWED, PERMISSION_DENIED_ERROR, TASK_NOT_EXIST_ERROR


async def upload_task_pic(
        id_user: int,
        id_project: int,
        id_task: int,
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

    task = db.query(Tasks).filter(Tasks.id_task==id_task, Tasks.id_project==id_project).first()
    if not task:
         raise TASK_NOT_EXIST_ERROR

    if picture.content_type in ALLOWED_CONTENT_TYPE:
        if task.picture != DEFAULT_TASK_PIC:   
            print(str(BASE_DIR) + task.picture)      
            remove(str(BASE_DIR) + task.picture)
        picture.filename = f"{time()}_{id_project}.{picture.content_type.split('/')[1]}"
        dest_path = f"{IMAGES_PROJECTS_DIR}/{id_project}/tasks/{picture.filename}"
        with open(dest_path, 'wb+') as dest:
            dest.write(picture.file.read())

        await compress_image(dest_path)

        new_path = ""
        for node in dest_path.split('/')[-5:]:
            new_path += f"/{node}"
            
        task.picture = new_path

        db.commit()
        db.refresh(task)

        task = TaskProjOutSchema.model_validate(task)
        subtasks = db.query(Subtasks).filter(Subtasks.id_task==task.id_task).all()
        subtasks = [SubtaskOutSchema.model_validate(subtask) for subtask in subtasks]
        task.subtasks = subtasks

        return task
    else: 
        raise IMAGE_TYPE_NOT_ALLOWED
    

async def delete_task_pic(
          id_user: int,
          id_project: int,
          id_task: int,
          db: db_dependency
):
    user = db.query(ProjectsUsers).filter(ProjectsUsers.id_project==id_project, ProjectsUsers.id_user==id_user).first()
    if user:
        if user.role != "owner":
            raise PERMISSION_DENIED_ERROR
    else:
            raise PERMISSION_DENIED_ERROR
    del user

    task = db.query(Tasks).filter(Tasks.id_task==id_task, Tasks.id_project==id_project).first()
    if not task:
         raise TASK_NOT_EXIST_ERROR
    
    if task.picture != DEFAULT_TASK_PIC:         
        remove(str(BASE_DIR) + task.picture)

    task.picture = DEFAULT_TASK_PIC
    
    db.commit()
    db.refresh(task)

    task = TaskProjOutSchema.model_validate(task)
    subtasks = db.query(Subtasks).filter(Subtasks.id_task==task.id_task).all()
    subtasks = [SubtaskOutSchema.model_validate(subtask) for subtask in subtasks]
    task.subtasks = subtasks

    return task
