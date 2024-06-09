from database.connection import db_dependency
from schemas.task import TaskProjInSchema, TaskProjOutSchema
from schemas.subtask import SubtaskOutSchema
from database.models import Projects, ProjectsUsers, Tasks, Subtasks
from errors.my_errors import PROJECT_NOT_EXIST_ERROR, PERMISSION_DENIED_ERROR, TASK_NOT_EXIST_ERROR
from os import remove
from file_system.settings import BASE_DIR, DEFAULT_TASK_PIC


async  def create_task(
        data: TaskProjInSchema,
        id_project: int,
        id_user: int,
        db: db_dependency
):
    """Метод создания проектной задачи."""
    project = db.query(ProjectsUsers).filter(ProjectsUsers.id_project==id_project, ProjectsUsers.id_user==id_user).first()
    if not project:
        raise PROJECT_NOT_EXIST_ERROR
    del project
    
    task = Tasks(
        title=data.title,
        description=data.description,
        start_date=data.start_date,
        end_date=data.end_date,
        done=data.done,
        rank=data.rank,
        category=data.category,
        id_project=id_project,
        id_user=id_user
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    task = TaskProjOutSchema.model_validate(task)
    subtasks = db.query(Subtasks).filter(Subtasks.id_task==task.id_task).all()
    subtasks = [SubtaskOutSchema.model_validate(subtask) for subtask in subtasks]
    task.subtasks = subtasks

    return task


async def update_task(
        data: TaskProjInSchema,
        id_project: int,
        id_task: int,
        id_user: int,
        db: db_dependency
):
    """Метод обновления проектной задачи."""
    project = db.query(ProjectsUsers).filter(ProjectsUsers.id_project==id_project, ProjectsUsers.id_user==id_user).first()
    if not project:
        raise PROJECT_NOT_EXIST_ERROR
    if project.role != "owner" and project.role != "editor":
        raise PERMISSION_DENIED_ERROR
    del project

    task = db.query(Tasks).filter(Tasks.id_task==id_task, Tasks.id_project==id_project).first()
    if not task:
        raise TASK_NOT_EXIST_ERROR
    
    task.title = data.title
    task.description = data.description
    task.start_date = data.start_date
    task.end_date = data.end_date
    task.done = data.done
    task.rank = data.rank
    task.category = data.category
    
    db.commit()
    db.refresh(task)
    
    return TaskProjOutSchema.model_validate(task)



async def delete_task(
        id_project: int,
        id_task: int,
        id_user: int,
        db: db_dependency
):
    """Метод удаления проектной задачи."""
    project = db.query(ProjectsUsers).filter(ProjectsUsers.id_project==id_project, ProjectsUsers.id_user==id_user).first()
    if not project:
        raise PROJECT_NOT_EXIST_ERROR
    if project.role != "owner" and project.role != "editor":
        raise PERMISSION_DENIED_ERROR
    del project


    task = db.query(Tasks).filter(Tasks.id_task==id_task, Tasks.id_project==id_project).first()
    if not task or task.id_project == None:
        raise TASK_NOT_EXIST_ERROR
    
    if task.picture != DEFAULT_TASK_PIC:         
        remove(str(BASE_DIR) + task.picture)

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}


async def get_task(
        id_project: int,
        id_task: int,
        id_user: int,
        db: db_dependency
):
    """Метод получения одной проектной задачи по идентификатору."""
    project = db.query(ProjectsUsers).filter(ProjectsUsers.id_project==id_project, ProjectsUsers.id_user==id_user).first()
    if not project:
        raise PROJECT_NOT_EXIST_ERROR
    del project

    task = db.query(Tasks).filter(Tasks.id_task==id_task, Tasks.id_project==id_project).first()
    if not task:
        raise TASK_NOT_EXIST_ERROR
    task = TaskProjOutSchema.model_validate(task)
    subtasks = db.query(Subtasks).filter(Subtasks.id_task==task.id_task).all()
    subtasks = [SubtaskOutSchema.model_validate(subtask) for subtask in subtasks]
    task.subtasks = subtasks

    return task


async def get_tasks(
        id_project: int,
        id_user: int,
        db: db_dependency
):
    """Метод получения всех проектных задач из заданного проекта."""
    project = db.query(ProjectsUsers).filter(ProjectsUsers.id_project==id_project, ProjectsUsers.id_user==id_user).first()
    if not project:
        raise PROJECT_NOT_EXIST_ERROR
    del project

    tasks = db.query(Tasks).filter(Tasks.id_project==id_project).all()
    tasks = [TaskProjOutSchema.model_validate(task) for task in tasks]
    for task in tasks:
        subtasks = db.query(Subtasks).filter(Subtasks.id_task==task.id_task).all()
        subtasks = [SubtaskOutSchema.model_validate(subtask) for subtask in subtasks]
        task.subtasks = subtasks
    
    return tasks