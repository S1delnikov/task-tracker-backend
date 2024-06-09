from fastapi import APIRouter, Depends
from typing import Annotated
from auth.jwthandler import get_current_user
from database.connection import db_dependency
from schemas.user import UserInSchema
from schemas.task import TaskSoloInSchema, TaskProjInSchema
import crud.tasks.task_solo as crud_solo
import crud.tasks.task_proj as crud_proj

router = APIRouter()

@router.post('/create_task_solo')
async def create_task_solo(
    data: TaskSoloInSchema,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_solo.create_task(data=data, id_user=current_user.id_user, db=db)


@router.put('/update_task_solo/{id_task}')
async def update_task_solo(
    id_task,
    data: TaskSoloInSchema,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_solo.update_task(data=data, id_task=id_task, id_user=current_user.id_user, db=db)


@router.delete('/delete_task_solo/{id_task}')
async def delete_task_solo(
    id_task,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_solo.delete_task(id_task=id_task, id_user=current_user.id_user, db=db)


@router.get('/get_solo_task/{id_task}')
async def get_solo_task(
    id_task,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_solo.get_task(id_task=id_task, id_user=current_user.id_user, db=db)


@router.get('/get_solo_tasks')
async def get_solo_tasks(
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_solo.get_tasks(id_user=current_user.id_user, db=db)


@router.post('/create_task_proj/{id_project}')
async def create_task_proj(
    id_project,
    data: TaskProjInSchema,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.create_task(data=data, id_project=id_project, id_user=current_user.id_user, db=db)


@router.put('/update_task_proj/{id_project}/{id_task}')
async def update_task_proj(
    id_project,
    id_task,
    data: TaskProjInSchema,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.update_task(data=data, id_project=id_project, id_task=id_task, id_user=current_user.id_user, db=db)


@router.delete('/delete_task_proj/{id_project}/{id_task}')
async def delete_task_proj(
    id_project,
    id_task,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.delete_task(id_project=id_project, id_task=id_task, id_user=current_user.id_user, db=db)


@router.get('/get_proj_task/{id_project}/{id_task}')
async def get_proj_task(
    id_project,
    id_task,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.get_task(id_project=id_project, id_task=id_task, id_user=current_user.id_user, db=db)


@router.get('/get_proj_tasks/{id_project}')
async def get_proj_tasks(
    id_project,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.get_tasks(id_project=id_project, id_user=current_user.id_user, db=db)