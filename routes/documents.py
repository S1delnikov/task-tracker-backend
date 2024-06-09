from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from typing import Annotated, List
from database.connection import db_dependency
from schemas.user import UserInSchema
from auth.jwthandler import get_current_user
import crud.documents.document as crud


router = APIRouter()


@router.post('/upload_document')
async def upload_document(
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    document: UploadFile,
    db: db_dependency
):
    return await crud.upload_document(id_user=current_user.id_user, document=document, db=db)


@router.post('/upload_documents')
async def upload_documents(
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    documents: List[UploadFile],
    db: db_dependency
):
    return await crud.upload_documents(id_user=current_user.id_user, documents=documents, db=db)


@router.put('/update_document_name/{id_document}/{new_name}')
async def update_document_name(
    id_document,
    new_name,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud.update_document_name(id_user=current_user.id_user, id_document=id_document, new_name=new_name, db=db)


@router.delete('/delete_document/{id_document}')
async def delete_document(
    id_document,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud.delete_document(id_user=current_user.id_user, id_document=id_document, db=db)


@router.post('/share_document/{id_document}/{new_user}')
async def share_document(
    id_document,
    new_user,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud.share_document(id_user=current_user.id_user, id_document=id_document, searchname=new_user, db=db)


@router.delete('/take_away_access/{id_document}/{id_user}')
async def take_away_access(
    id_document,
    id_user,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud.take_away_access(id_owner=current_user.id_user, id_document=id_document, id_user=id_user, db=db)


@router.delete('/refuse_the_document/{id_document}')
async def refuse_the_document(
    id_document,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud.refuse_the_document(id_user=current_user.id_user, id_document=id_document, db=db)


@router.get('/get_documents')
async def get_document_users(
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud.get_documents(id_user=current_user.id_user, db=db)


@router.get('/get_document_users/{id_document}')
async def get_document_users(
    id_document,
    current_user: Annotated[UserInSchema, Depends(get_current_user)],
    db: db_dependency
):
    return await crud.get_document_users(id_user=current_user.id_user, id_document=id_document, db=db)
