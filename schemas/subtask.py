from pydantic import BaseModel


class SubtaskSchema(BaseModel):
    """Представление подзадачи \n
    title: str
    description: str
    done: bool = False\n

    class Config:
        from_attributes = True
    """
    title: str
    description: str
    done: bool = False

    class Config:
        from_attributes = True


class SubtaskOutSchema(BaseModel):
    """Представление исходящей модели подзадачи\n
    id_subtask: int
    title: str
    description: str
    done: bool = False\n

    class Config:
        from_attributes = True
    """
    id_subtask: int
    title: str
    description: str
    done: bool = False

    class Config:
        from_attributes = True
