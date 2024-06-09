from pydantic import BaseModel


class DocumentSchema(BaseModel):
    """Представление входящей модели проекта"""
    id_document: int
    name: str 
    path: str

    class Config:
        from_attributes = True