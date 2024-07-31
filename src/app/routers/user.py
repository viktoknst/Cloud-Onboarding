from fastapi import APIRouter, HTTPException, Depends

from app.special.config import ENDPOINTS

from app.external_dependencies.db_interface import DBProxy
from app.schemas.user import UserCreate
from app.crud.user_crud import User
from app.routers.login import get_user_dependency

user_router = APIRouter()

User.set_db(DBProxy.get_instance().get_db())

@user_router.post(ENDPOINTS['user'])
def create_user(u: UserCreate):
    '''
    Endpoint for creating users in db.
    '''
    try:
        user = User.create(u.user_name, u.password)
    except ValueError as ex:
        raise HTTPException(409, "Failed to create user: " + str(ex)) from ex
    except Exception as ex:
        raise HTTPException(500, "Failed to create user: " + str(ex)) from ex
    return {'msg': 'User created', 'user': user.to_dict()}


@user_router.get(ENDPOINTS['user'])
def read_user(user: User = Depends(get_user_dependency)):
    '''
    Endpoint for reading users from db.
    '''
    return {"user": user.to_dict()}


@user_router.put(ENDPOINTS['user'])
def update_user(u: UserCreate, user: User = Depends(get_user_dependency)):
    user.name = u.user_name
    user.change_password(u.password)
    try:
        user.update()
    except ValueError as ex:
        raise HTTPException(409, detail='Failed to update user') from ex
    except Exception as ex:
        raise HTTPException(500, detail="Failed to update user: " + str(ex)) from ex
    return {'msg': 'User updated, login required', 'user': user.to_dict()}


@user_router.delete(ENDPOINTS['user'])
def delete_user(user: User = Depends(get_user_dependency)):
    '''
    Endpoint for deleting users from db.
    '''
    try:
        user.delete()
    except Exception as ex:
        raise HTTPException(500, detail='Failed to delete user') from ex
    return {'msg': 'User deleted', 'user': user.to_dict()}
