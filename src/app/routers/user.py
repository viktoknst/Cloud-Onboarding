from fastapi import APIRouter, HTTPException, Depends

from app.special.config import ENDPOINTS

from app.external_dependencies.db_interface import DBProxy
from app.schemas.user import UserCreate
from app.crud.user_crud import User
from app.routers.login import get_current_user

user_router = APIRouter()

User.set_db(DBProxy.get_instance().get_db())


@user_router.post(ENDPOINTS['user'])
def create_user(u: UserCreate):
    '''
    Endpoint for creating users in db.
    '''
    try:
        user = User.create(u.user_name, u.password)
    except Exception as ex:
        raise HTTPException(409, "Failed to create user") from ex
    return {'msg': 'User created', 'user': user.to_jsons()}


@user_router.get(ENDPOINTS['user'])
def read_user(user_name: str = Depends(get_current_user)):
    '''
    Endpoint for reading users from db.
    '''
    try:
        user = User.read(name=user_name)
    except Exception as ex:
        raise HTTPException(404) from ex
    return user.to_jsons()


@user_router.put(ENDPOINTS['user'])
def update_user(u: UserCreate, user_name: str = Depends(get_current_user)):
    try:
        user = User.read(name=user_name)
    except Exception as ex:
        raise HTTPException(404, detail='Failed to update user: user does not exist') from ex
    user.name = u.user_name
    user.change_password(u.password)
    try:
        user.update()
    except Exception as ex:
        raise HTTPException(404, detail='Failed to update user') from ex
    return {'msg': 'User updated, login required', 'user': user.to_jsons()}


@user_router.delete(ENDPOINTS['user'])
def delete_user(user_name: str = Depends(get_current_user)):
    '''
    Endpoint for deleting users from db.
    '''
    try:
        user = User.read(name=user_name)
        user.delete()
    except Exception as ex:
        raise HTTPException(404, detail='Failed to delete user: user does not exist') from ex
    return {'msg': 'User deleted', 'user': user.to_jsons()}
