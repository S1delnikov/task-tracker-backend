from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from datetime import timedelta
from auth.users import authenticate_user
from auth.jwthandler import ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme, create_access_token, get_current_user
from auth.users import get_password_hash
from schemas.token import Token
from schemas.user import UserInSchema, UserRegSchema, UserUpdateSchema
from database.connection import db_dependency
from database.models import Users
import crud.users.user as crud

router = APIRouter()

@router.get('/')
def home():
    return {'data': 'Hello, stranger'}


@router.post('/login')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    return await crud.login(form_data.username, form_data.password, db)


@router.post('/register')
async def register(data: UserRegSchema, db: db_dependency):
    return await crud.create_user(data, db)

@router.get('/check')
def check(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@router.get('/about')
async def about(
    current_user: Annotated[UserInSchema, Depends(get_current_user)], 
    db: db_dependency
):
    return await crud.about(id_user=current_user.id_user, db=db)


@router.get('/about/{id_project}')
async def about_rights(
    id_project,
    current_user: Annotated[UserInSchema, Depends(get_current_user)], 
    db: db_dependency
):
    return await crud.about_rights(id_user=current_user.id_user, id_project=id_project, db=db)


@router.put('/update_user_info')
async def update_user_info(
    current_user: Annotated[UserInSchema, Depends(get_current_user)], 
    data: UserUpdateSchema,
    db: db_dependency
):
    return await crud.update_user_info(id_user=current_user.id_user, data=data, db=db)


@router.delete('/delete_user')
async def delete_user(
    current_user: Annotated[UserInSchema, Depends(get_current_user)], 
    db: db_dependency
):
    return await crud.delete_user(id_user=current_user.id_user, db=db)