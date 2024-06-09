from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from time import time


class UserRegSchema(BaseModel):
    """Представление модели регистрирующегося пользователя\n
    username: str
    email: str | None = None
    password: str
    date_of_registration: datetime = datetime.now()\n

    class Config:
        from_attributes = True
    """
    username: str
    searchname: str = time()
    password: str
    date_of_registration: datetime = datetime.now()

    class Config:
        from_attributes = True


class UserInSchema(BaseModel):
    """Представление модели входящих данных пользователя\n
    id_user: int
    username: str
    password: str\n

    class Config:
        from_attributes = True
    """
    id_user: int
    username: str
    password: str

    class Config:
        from_attributes = True


class UserUpdateSchema(BaseModel):
    searchname: str
    full_name: str
    disabled: bool

    class Config:
        from_attributes = True


class UserOutSchema(BaseModel):
    """Представление модели исходящих данных пользователя\n
    id_user: int
    username: str\n

    class Config:
        from_attributes = True
    """
    id_user: int
    # username: str
    searchname: str
    full_name: str
    disabled: bool
    # email: str
    picture: str

    class Config:
        from_attributes = True