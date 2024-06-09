from sqlalchemy import text
from database.connection import db_dependency
from database.models import Users, Documents, UsersDocuments
from schemas.user import UserOutSchema
from schemas.document import DocumentSchema
from typing import List
from time import time
from shutil import rmtree
from os import remove
from file_system.settings import DOCUMENTS_DIR, TEMP_DIR, BASE_DIR
from file_system.methods import compress_file, compress_files
from errors.my_errors import FILE_IS_NOT_EXIST, PERMISSION_DENIED_ERROR, USER_NOT_EXIST_ERROR, USER_IS_ALREADY_HAS_FILE, SUICIDE_IS_NOT_A_WAY_OUT
from fastapi import UploadFile


async def upload_document(
      id_user: int,
      document: UploadFile,
      db: db_dependency
):
      print(document.content_type)
      old_filename = document.filename
      temp_path = f"{TEMP_DIR}/{id_user}/{old_filename}"
      temp_dir = f"{TEMP_DIR}/{id_user}"
      document.filename = f"{time()}_{id_user}.zip"
      zip_path = f"{DOCUMENTS_DIR}/{id_user}/{document.filename}"
      with open(temp_path, 'wb+') as dest: ######
            dest.write(document.file.read())
      await compress_file(file_path=temp_path, zip_path=zip_path, filename=old_filename)

      rmtree(temp_dir)
      TEMP_DIR.joinpath(str(id_user)).mkdir()
    
      new_path = ""
      for node in zip_path.split('/')[-3:]:
            new_path += f"/{node}"

      print(new_path)
      document = Documents(
            name = old_filename,
            path = new_path
      )
      db.add(document)
      db.commit()
      db.refresh(document)

      user_document = UsersDocuments(
            id_user = id_user,
            id_document = document.id_document
      )
      db.add(user_document)
      db.commit()
      db.refresh(user_document)

      return {'document': DocumentSchema.model_validate(document), 'user_document': user_document}


async def upload_documents(
      id_user: int,
      documents: List[UploadFile],
      db: db_dependency
):
      temp_paths = []
      old_filenames = [doc.filename for doc in documents]
      for old_filename in old_filenames:
            temp_path = f"{TEMP_DIR}/{id_user}/{old_filename}"
            temp_paths.append(temp_path)
      
      temp_dir = f"{TEMP_DIR}/{id_user}"
      zip_path = f"{DOCUMENTS_DIR}/{id_user}/{time()}_{id_user}.zip"

      for index, temp_path in enumerate(temp_paths):
            with open(temp_path, 'wb+') as dest:
                  dest.write(documents[index].file.read())
      await compress_files(file_paths=temp_paths, zip_path=zip_path, filenames=old_filenames)

      rmtree(temp_dir)

      TEMP_DIR.joinpath(str(id_user)).mkdir()
    
      new_path = ""
      for node in zip_path.split('/')[-3:]:
            new_path += f"/{node}"

      document = Documents(
            name = str(old_filenames),
            path = new_path
      )
      db.add(document)
      db.commit()
      db.refresh(document)

      user_document = UsersDocuments(
            id_user = id_user,
            id_document = document.id_document
      )
      db.add(user_document)
      db.commit()
      db.refresh(user_document)

      return {'document': DocumentSchema.model_validate(document), 'user_document': user_document}


async def update_document_name(
      id_user: int,
      id_document: int,
      new_name: str,
      db: db_dependency
):
      document = db.query(Documents)\
                  .join(UsersDocuments, UsersDocuments.id_document==Documents.id_document)\
                  .filter(UsersDocuments.id_user==id_user, UsersDocuments.role=='owner') \
                  .first()
      if document:
            document.name = new_name
            db.commit()
            db.refresh(document)

            return document
      return 



async def delete_document(
      id_user: int,
      id_document: int,
      db: db_dependency
):
      row = db.query(UsersDocuments).filter(UsersDocuments.id_user==id_user, UsersDocuments.id_document==id_document).first()
      if not row:
            raise FILE_IS_NOT_EXIST
      if row.role != "owner":
            raise PERMISSION_DENIED_ERROR
      del row 

      document = db.query(Documents).filter(Documents.id_document==id_document).first()
      remove(str(BASE_DIR) + document.path)
      db.delete(document)
      db.commit()
      
      return DocumentSchema.model_validate(document)


async def share_document(
      id_user: int,
      id_document: int,
      searchname: str,
      db: db_dependency
):
      row = db.query(UsersDocuments).filter(UsersDocuments.id_user==id_user, UsersDocuments.id_document==id_document).first()
      if not row:
            raise FILE_IS_NOT_EXIST
      if row.role != "owner":
            raise PERMISSION_DENIED_ERROR
      del row 

      user = db.query(Users).filter(Users.searchname==searchname, Users.disabled==True).first()
      if not user:
            raise USER_NOT_EXIST_ERROR

      exist = db.query(UsersDocuments).filter(UsersDocuments.id_user==user.id_user, UsersDocuments.id_document==id_document).first()
      if exist:
            raise USER_IS_ALREADY_HAS_FILE

      new__user_document = UsersDocuments(
            id_user = user.id_user,
            id_document = id_document,
            role = "editor"
      )
      db.add(new__user_document)
      db.commit()
      # db.refresh(new__user_document)

      return UserOutSchema.model_validate(user)


async def take_away_access(
      id_owner: int,
      id_document: int,
      id_user: int,
      db: db_dependency
):
      owner = db.query(UsersDocuments).filter(UsersDocuments.id_user==id_owner, UsersDocuments.id_document==id_document, UsersDocuments.role=='owner').first()
      if not owner:
            raise PERMISSION_DENIED_ERROR
      del owner

      user = db.query(UsersDocuments).filter(UsersDocuments.id_user==id_user, UsersDocuments.id_document==id_document).first()
      if not user: 
            raise USER_NOT_EXIST_ERROR
      
      db.delete(user)
      db.commit()

      return user


async def refuse_the_document(
      id_user: int,
      id_document: int,
      db: db_dependency
):
      rights = db.query(UsersDocuments).filter(UsersDocuments.id_document==id_document, UsersDocuments.id_user==id_user).first()

      if not rights:
            raise FILE_IS_NOT_EXIST

      if rights.role == 'owner':
            raise SUICIDE_IS_NOT_A_WAY_OUT
      
      db.delete(rights)
      db.commit()

      return rights


async def get_documents(
      id_user: int,
      db: db_dependency      
):
      row = db.query(UsersDocuments).filter(UsersDocuments.id_user==id_user).first()
      if not row:
            return {'documents': []}
      del row

      query = text(" \
                  select documents.id_document, documents.name, documents.path, users_documents.role from documents \
                  join users_documents ON users_documents.id_document = documents.id_document \
                  where users_documents.id_user=:id_user \
                   ")
      documents = db.execute(query, {'id_user': id_user})
      documents = [dict(id_document=doc.id_document, name=doc.name, path=doc.path, role=doc.role) for doc in documents]

      return {'documents': documents}


async def get_document_users(
      id_user: int,
      id_document: int,
      db: db_dependency
):
      row = db.query(UsersDocuments).filter(UsersDocuments.id_user==id_user).first()
      if row.role != 'owner':
            raise PERMISSION_DENIED_ERROR
      del row

      query = text("\
                        select users.id_user, users.searchname, users.full_name from users \
                        join users_documents ON users_documents.id_user = users.id_user \
                        where users_documents.id_document = :id_document and users_documents.id_user != :id_user \
                  ")
      users = db.execute(query, {'id_document': id_document, 'id_user': id_user})
      users = [dict(id_user=user.id_user, searchname=user.searchname, full_name=user.full_name) for user in users]

      return {'users': users}


