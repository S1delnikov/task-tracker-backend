from fastapi import APIRouter, Depends
from typing import Annotated
from auth.jwthandler import get_current_user
from database.connection import db_dependency
from schemas.project import ProjectInSchema
from schemas.user import UserInSchema
import crud.projects.project as crud_proj


router = APIRouter()

@router.post('/create_proj')
async def create_proj(
    data: ProjectInSchema,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.create_proj(data=data, id_user=current_user.id_user, db=db)


@router.get('/get_projects')
async def get_projects(
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.get_projects(id_user=current_user.id_user, db=db)


@router.put('/update_proj/{id_project}')
async def update_proj(
    id_project,
    data: ProjectInSchema,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.update_proj(data=data, id_project=id_project, id_user=current_user.id_user, db=db)


@router.delete('/delete_proj/{id_project}')
async def delete_proj(
    id_project,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.delete_proj(id_project=id_project, id_user=current_user.id_user, db=db)


@router.delete('/leave_proj/{id_project}')
async def leave_project(
    id_project,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.leave_proj(id_project=id_project, id_user=current_user.id_user, db=db)


@router.post('/add_member/{id_project}/{searchname}')
async def add_member(
    id_project,
    searchname,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency,
    role: str = "editor"
):
    return await crud_proj.add_member(id_project=id_project, id_user=current_user.id_user, searchname=searchname, role=role, db=db)


@router.delete('/delete_member/{id_project}/{id_member}')
async def delete_member(
    id_project, 
    id_member,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.delete_member(id_project=id_project, id_user=current_user.id_user, id_member_on_delete=id_member, db=db)


@router.get('/get_members/{id_project}')
async def get_members(
    id_project,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.get_members(id_project=id_project, db=db)


@router.get('/get_member/{id_project}/{id_member}')
async def get_members(
    id_project,
    id_memeber,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud_proj.get_member(id_project=id_project, id_user=id_memeber, db=db)