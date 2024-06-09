"""

    Данный модуль содержит в себе описания таблиц, 
    которые будут созданы при первом подключении к базе данных

"""

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from .settings import Base


class Users(Base):
    """Таблица пользователей"""
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    searchname = Column(String, index=True, unique=True)
    full_name = Column(String, default="")
    email = Column(String, default="")
    password = Column(String)
    disabled = Column(Boolean, default=False)
    date_of_registration = Column(DateTime)
    picture = Column(String, default="/images/default/profile_pic/profile_pic.jpeg")


class Friends(Base):
    """Таблица друзей пользователя"""
    __tablename__ = 'friends'

    id_sender = Column(Integer, ForeignKey('users.id_user', ondelete="CASCADE"), primary_key=True)
    id_recipient = Column(Integer, ForeignKey('users.id_user', ondelete="CASCADE"), primary_key=True)
    relation_type = Column(String, default="")


class Tasks(Base):
    """Таблица задач"""
    __tablename__ = 'tasks'

    id_task = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="")
    description = Column(String, default="")
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    done = Column(Boolean, default=False)
    rank = Column(String, default="")
    category = Column(String, default="")
    picture = Column(String, default="/images/default/task_pic/task_pic.jpeg")
    id_project = Column(Integer, ForeignKey("projects.id_project", ondelete="CASCADE"), default=None)
    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"))


class Subtasks(Base):
    """Таблица подзадач"""
    __tablename__ = 'subtasks'

    id_subtask = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="")
    description = Column(String, default="")
    done = Column(Boolean, default=False)
    id_task = Column(Integer, ForeignKey("tasks.id_task", ondelete="CASCADE"))


class Projects(Base):
    """Таблица проектов"""
    __tablename__ = 'projects'

    id_project = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="")
    description = Column(String, default="")
    picture = Column(String, default="/images/default/project_pic/project_pic.jpg")


class ProjectsUsers(Base):
    """Таблица-посредник между пользователями и проектами"""
    __tablename__ = 'projects_users'

    id_project = Column(Integer, ForeignKey("projects.id_project", ondelete="CASCADE"), primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"), primary_key=True)
    role = Column(String, default="owner")


class Documents(Base):
    """Таблица документов"""
    __tablename__ = 'documents'

    id_document = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="doc")
    path = Column(String, default="")


class UsersDocuments(Base):
    """Таблица-посредник между пользователями и документами"""
    __tablename__ = 'users_documents'
    id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"), primary_key=True)
    id_document = Column(Integer, ForeignKey("documents.id_document", ondelete="CASCADE"), primary_key=True)
    role = Column(String, default="owner")



# class Messages(Base):
#     """Таблица сообщений пользователей"""
#     __tablename__ = 'messages'

#     id_message = Column(Integer, primary_key=True, index=True)
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)
#     id_project = Column(Integer, ForeignKey("projects.id_project", ondelete="CASCADE"))
#     id_user = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"))


# class Contents(Base):
#     """Таблица с содержимым сообщений пользователя"""
#     __tablename__ = 'contents'

#     id_content = Column(Integer, primary_key=True, index=True)
#     text = Column(String, default="")
#     image = Column(String, default="") # путь к изображению
#     id_message = Column(Integer, ForeignKey("messages.id_message", ondelete="CASCADE"))

