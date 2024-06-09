from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from typing import Annotated
from database.connection import db_dependency
from schemas.user import UserInSchema
from auth.jwthandler import get_current_user
import crud.users.picture as crud_user
import crud.projects.picture as crud_proj
import crud.tasks.picture as crud_tasks

router = APIRouter()

@router.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    print(file)
    return {"file_size": len(file)}
    # return file

@router.post("/upload_profile_pic/")
async def upload_profile_pic(
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    picture: UploadFile,
    db: db_dependency
):
    return await crud_user.upload_profile_pic(id_user=current_user.id_user, picture=picture, db=db)


@router.delete('/delete_profile_pic')
async def delete_profile_pic(
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_user.delete_profile_pic(id_user=current_user.id_user, db=db)


@router.get('/get_profile_pic')
async def get_profile_pic(
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_user.get_profile_pic(id_user=current_user.id_user, db=db)


@router.post('/upload_project_pic/{id_project}')
async def upload_project_pic(
    id_project,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    picture: UploadFile,
    db: db_dependency
):
    return await crud_proj.upload_project_pic(id_user=current_user.id_user, id_project=id_project, picture=picture, db=db)


@router.delete('/delete_project_pic/{id_project}')
async def delete_project_pic(
    id_project,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.delete_project_pic(id_user=current_user.id_user, id_project=id_project, db=db)


@router.post('/upload_task_pic/{id_project}/{id_task}')
async def upload_task_pic(
    id_project, 
    id_task,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    picture: UploadFile,
    db:db_dependency
):
    return await crud_tasks.upload_task_pic(id_user=current_user.id_user, id_project=id_project, id_task=id_task, picture=picture, db=db)


@router.delete('/delete_task_pic/{id_project}/{id_task}')
async def delete_project_pic(
    id_project,
    id_task,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_tasks.delete_task_pic(id_user=current_user.id_user, id_project=id_project, id_task=id_task, db=db)