from pydantic import BaseModel
from datetime import datetime
from typing import List
from .subtask import SubtaskOutSchema

class TaskSoloInSchema(BaseModel):
    """Представление одиночной входящей задачи\n
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    done: bool = False\n
    class Config:
        from_attributes = True
    """
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    done: bool = False
    class Config:
        from_attributes = True


class TaskSoloOutSchema(BaseModel):
    """Представление одиночной исходящей задачи\n
    id_task: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    done: bool = False
    subtasks: List[SubtaskOutSchema] = None\n
    
    class Config:
        from_attributes = True
    """
    id_task: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    done: bool = False
    picture: str
    subtasks: List[SubtaskOutSchema] = None
    
    class Config:
        from_attributes = True


class TaskProjInSchema(BaseModel):
    """Представление проектной входящей задачи\n
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    done: bool = False
    rank: str = ""
    category: str = "Надо сделать"\n

    class Config:
        from_attributes = True
    """
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    done: bool = False
    rank: str = ""
    category: str = "Надо сделать"

    class Config:
        from_attributes = True


class TaskProjOutSchema(BaseModel):
    """Представление проектной исходящей задачи\n
    id_task: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    done: bool = False
    rank: str = ""
    category: str = "Надо сделать"
    id_project: int
    id_user: int
    subtasks: List[SubtaskOutSchema] = None\n

    class Config:
        from_attributes = True
    """
    id_task: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    done: bool = False
    rank: str = ""
    category: str = "Надо сделать"
    picture: str
    id_project: int
    id_user: int
    subtasks: List[SubtaskOutSchema] = None

    class Config:
        from_attributes = True