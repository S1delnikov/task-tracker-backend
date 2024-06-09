from fastapi import HTTPException, status
from datetime import timedelta
from shutil import rmtree
from database.connection import db_dependency
from sqlalchemy.sql import text
from auth.jwthandler import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from auth.users import get_password_hash, authenticate_user
from schemas.user import UserRegSchema, UserOutSchema, UserUpdateSchema
from schemas.project import ProjectUserOutSchema
from schemas.token import Token
from database.models import Users, ProjectsUsers
from file_system.settings import IMAGES_USERS_DIR, DOCUMENTS_DIR, TEMP_DIR
from errors.my_errors import USERNAME_IS_OCCUPIED_ERROR, INCORRECT_UN_OR_PSWD_ERROR

async def create_user(data: UserRegSchema, db: db_dependency):
    try:
        new_user = Users (
            username=data.username,
            searchname = data.searchname,
            password=get_password_hash(password=data.password),
            date_of_registration=data.date_of_registration
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        IMAGES_USERS_DIR.joinpath(str(new_user.id_user)).mkdir()
        DOCUMENTS_DIR.joinpath(str(new_user.id_user)).mkdir()
        TEMP_DIR.joinpath(str(new_user.id_user)).mkdir()
    except: 
        raise USERNAME_IS_OCCUPIED_ERROR
    # return UserOutSchema(id_user=new_user.id_user, username=new_user.username, email=new_user.email, picture=new_user.picture)
    return UserOutSchema.model_validate(new_user)


async def login(username, password: str, db: db_dependency):
    user = authenticate_user(username=username, password=password, db=db)
    if not user:
        raise INCORRECT_UN_OR_PSWD_ERROR
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={ "sub": user.username }, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


async def about(
       id_user: int,
       db: db_dependency 
):    
    user = db.query(Users).filter(Users.id_user == id_user).first()
    return UserOutSchema.model_validate(user)
    

async def about_rights(
       id_user: int,
       id_project: int,
       db: db_dependency 
):
    user = db.query(Users).filter(Users.id_user == id_user).first()
    rights = db.query(ProjectsUsers).filter(ProjectsUsers.id_project==id_project, ProjectsUsers.id_user==id_user).first()
    return {"user": UserOutSchema.model_validate(user), "rights": ProjectUserOutSchema.model_validate(rights)}


async def update_user_info(
        id_user: int,
        data: UserUpdateSchema,
        db: db_dependency
):
    try:
        user = db.query(Users).filter(Users.id_user == id_user).first()
        user.searchname = data.searchname
        user.full_name = data.full_name
        user.disabled = data.disabled
        
        db.commit()
        db.refresh(user)

        return UserOutSchema.model_validate(user)
    except:
        raise USERNAME_IS_OCCUPIED_ERROR


async def delete_user(
        id_user: int,
        db: db_dependency
):
    user = db.query(Users).filter(Users.id_user==id_user).first()

    delete_query = text('\
                            delete from documents\
                            using users_documents where users_documents.id_document = documents.id_document and users_documents.id_user = :id_user and users_documents.role=:role;\
                            delete from projects\
                            using projects_users where projects_users.id_project = projects.id_project and  projects_users.id_user = :id_user and projects_users.role=:role;\
                        ')

    db.execute(delete_query, {'id_user': id_user, 'role': 'owner'})
    db.delete(user)
    db.commit()
    
    rmtree(f"{IMAGES_USERS_DIR}/{id_user}")
    rmtree(f"{DOCUMENTS_DIR}/{id_user}")
    rmtree(f"{TEMP_DIR}/{id_user}")

    return UserOutSchema.model_validate(user)
