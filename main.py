from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# import schemas
from typing import Annotated
# import models
from database.settings import engine, SessionLocal
from database import models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from auth import jwthandler
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from routes import users, tasks, subtasks, projects, pictures, documents

from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://192.168.0.103:8080"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

static_folder_images = 'images'
static_folder_documents = 'documents'

app.mount('/images', StaticFiles(directory=static_folder_images))
app.mount('/documents', StaticFiles(directory=static_folder_documents))

models.Base.metadata.create_all(bind=engine)


app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(subtasks.router)
app.include_router(projects.router)
app.include_router(pictures.router)
app.include_router(documents.router)