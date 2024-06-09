from fastapi import APIRouter, Depends
from typing import Annotated
from auth.jwthandler import get_current_user
from database.connection import db_dependency
from schemas.subtask import SubtaskSchema
from schemas.user import UserInSchema
import crud.subtasks.subtask as crud


router = APIRouter()

@router.post('/create_subtask/{id_task}')
async def create_subtask(
    id_task,
    data: SubtaskSchema,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud.create_subtask(data=data, id_task=id_task, db=db)


@router.put('/update_subtask/{id_subtask}')
async def update_subtask(
    id_subtask,
    data: SubtaskSchema,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud.update_subtask(data=data, id_subtask=id_subtask, id_user=current_user.id_user, db=db)


@router.delete('/delete_subtask/{id_subtask}')
async def delete_subtask(
    id_subtask,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud.delete_subtask(id_subtask=id_subtask, id_user=current_user.id_user, db=db)