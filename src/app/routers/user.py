from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.special.config import ENDPOINTS

from app.external_dependencies.db_interface import DBProxy
from pymongo.database import Database
from app.models.user import User
from app.schemas.user import *
import app.crud.user as user_crud


user_router = APIRouter()


@user_router.post(ENDPOINTS['create_user'])
def create_user(u: UserCreate):
    db: Database = DBProxy.get_instance().get_db()
    result = user_crud.create(db, u.user_name)
    if result != None:
        raise HTTPException(409, result)
    return {'msg': 'User created'}


@user_router.get(ENDPOINTS['user'])
def read_user():
    pass


@user_router.put(ENDPOINTS['user'])
def update_user():
    pass


@user_router.delete(ENDPOINTS['user'])
def delete_user():
    pass
