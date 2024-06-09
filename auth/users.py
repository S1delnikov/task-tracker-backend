from fastapi import HTTPException, status, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database.models import Users
from database.connection import db_dependency


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str, db: db_dependency):
    user = db.query(Users).filter(Users.username==username).first()
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

def authenticate_user(username, password: str, db: db_dependency):
    user = get_user(username, db)
    if user:
        if verify_password(password, user.password):
            return user
        
