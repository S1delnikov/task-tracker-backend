from pydantic import BaseModel


class ProjectInSchema(BaseModel):
    """Представление входящей модели проекта\n
    name: str
    description: str\n

    class Config:
        from_attributes = True
    """
    name: str
    description: str

    class Config:
        from_attributes = True


class ProjectOutSchema(BaseModel):
    """Представление исходящей модели проекта\n
    id_project: int
    name: str
    description: str\n

    class Config:
        from_attributes = True
    """
    id_project: int
    name: str
    description: str
    picture: str

    class Config:
        from_attributes = True


class ProjectUserOutSchema(BaseModel):
    """Представление исходящей модели связи пользователя с проектом\n
    id_project: int
    id_user: int
    role: str\n

    class Config:
        from_attributes = True
    """
    id_project: int
    id_user: int
    role: str

    class Config:
        from_attributes = True