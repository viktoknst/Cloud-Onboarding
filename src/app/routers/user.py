from fastapi import APIRouter, HTTPException, Depends

from pymongo.database import Database

from app.special.config import ENDPOINTS

from app.external_dependencies.db_interface import DBProxy
#from app.models.user import User
from app.schemas.user import UserCreate, UserDelete
from app.crud import user_crud
from app.routers.login import get_current_user

user_router = APIRouter()


@user_router.post(ENDPOINTS['user'])
def create_user(u: UserCreate):
    '''
    Endpoint for creating users in db.
    '''
    db = DBProxy.get_instance().get_db()
    try:
        user_crud.create(db, u.user_name, u.password)
    except Exception as ex:
        raise HTTPException(409, "Failed to create user") from ex
    return {'msg': 'User created'}


@user_router.get(ENDPOINTS['user'])
def read_user(user_name: str = Depends(get_current_user)):
    '''
    Endpoint for reading users from db.
    '''
    db: Database = DBProxy.get_instance().get_db()
    try:
        user = user_crud.read(db, user_name=user_name)
    except Exception as ex:
        raise HTTPException(404) from ex
    return user


#@user_router.put(ENDPOINTS['user'])
#def update_user(body: UpdateUsers):
#    pass


@user_router.delete(ENDPOINTS['user'])
def delete_user(body: UserDelete):
    '''
    Endpoint for deleting users from db.
    '''
    db = DBProxy.get_instance().get_db()
    try:
        user_crud.delete(db, body.id)
    except Exception as ex:
        raise HTTPException(404, detail='Failed to delete user: user does not exist') from ex
    return {'msg': 'User deleted'}
