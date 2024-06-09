from fastapi import HTTPException, status
from schemas.subtask import SubtaskSchema
from database.models import Tasks, Subtasks, Users
from database.connection import db_dependency
from errors.my_errors import TASK_NOT_EXIST_ERROR, SUBTASK_NOT_EXIST_ERROR


async def create_subtask(data: SubtaskSchema, id_task: int, db: db_dependency):
    """Метод создания подзадачи. Работает для одиночных задач и проектных задач."""

    task = db.query(Tasks).filter(Tasks.id_task==id_task).first()
    if not task:
        raise TASK_NOT_EXIST_ERROR
    del task
    subtask = Subtasks (
        title = data.title,
        description = data.description,
        done = data.done,
        id_task = id_task
    )
    db.add(subtask)
    db.commit()
    db.refresh(subtask)
    
    return subtask


async def update_subtask(data: SubtaskSchema, id_subtask: int, id_user, db: db_dependency):
    """
    Метод обновления подзадачи. Работает для одиночных задач и проектных задач.
    
    SELECT subtasks.id_subtask, subtasks.title, subtasks.description, subtasks.done FROM subtasks\n
    JOIN tasks on tasks.id_task = subtasks.id_task\n
    JOIN users on tasks.id_user = users.id_user\n
    WHERE users.id_user = current_user.id_user AND subtasks.id_subtask = subtask_on_update.id_subtask;

    """
    
    subtask = \
        db.query(Subtasks) \
        .join(Tasks, Tasks.id_task==Subtasks.id_task) \
        .join(Users, Users.id_user==Tasks.id_user) \
        .filter(Subtasks.id_subtask==id_subtask) \
        .first()
    
    if not subtask:
        raise SUBTASK_NOT_EXIST_ERROR
    
    subtask.title = data.title
    subtask.description = data.description
    subtask.done = data.done

    db.commit()
    db.refresh(subtask)

    return subtask


async def delete_subtask(id_subtask, id_user: int, db: db_dependency):
    """Метод удаления подзадачи."""
    subtask = \
        db.query(Subtasks) \
        .join(Tasks, Tasks.id_task==Subtasks.id_task) \
        .join(Users, Users.id_user==Tasks.id_user) \
        .filter(Subtasks.id_subtask==id_subtask) \
        .first()
    
    if not subtask:
        raise SUBTASK_NOT_EXIST_ERROR
    
    db.delete(subtask)
    db.commit()
    
    return {"message": "Subtask deleted successfully."}