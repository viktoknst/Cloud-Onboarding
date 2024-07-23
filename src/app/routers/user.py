from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.special.config import ENDPOINTS

from app.external_dependencies.db_interface import DBProxy
from app.models.user import User
from app.schemas.user import *
import app.crud.user_crud as user_crud


user_router = APIRouter()


@user_router.post(ENDPOINTS['user'])
def create_user(u: UserCreate):
    db = DBProxy.get_instance().get_db()
    result = user_crud.create(db, u.user_name, u.password)
    if result is not None:
        raise HTTPException(409, result)
    return {'msg': 'User created'}


#@user_router.get(ENDPOINTS['user'])
#def read_user(u: UserRead):
#    db: Database = DBProxy.get_instance().get_db()
#    result = user_crud.read(db, u.id)
#    if isinstance(result, str):
#        raise HTTPException(404, result)
#    return User(result.id, result.name)


@user_router.put(ENDPOINTS['user'])
def update_user(body: UpdateUsers):
    pass


@user_router.delete(ENDPOINTS['user'])
def delete_user(body: UserDelete):
    db = DBProxy.get_instance().get_db()
    result = user_crud.delete(db, body.id)
    if result != None:
        raise HTTPException(400, result)
    return {'msg': 'User deleted'}
