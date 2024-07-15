from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.config import ENDPOINTS
from src.config import USER_DB


user_router = APIRouter()

class UserCreate(BaseModel):
    user_name: str

class User(BaseModel):
    user_name: str


@user_router.post(ENDPOINTS['create_user'])
def post_create_user(u: UserCreationRequest):
    if re.match(r'^[a-zA-Z0-9_-]{4,16}$', u.user_name) == None:
        raise HTTPException(409, "Username is invalid")

    if os.path.exists(USER_DB['user_dir']+"/"+u.user_name):
        raise HTTPException(409, "Username is in use!")

    os.mkdir(USER_DB['user_dir']+"/"+u.user_name)
    return {'msg': 'User created'}


@smt_router.post()
def rsrc_create():
    pass
@smt_router.get()
def rsrc_read():
    pass
@smt_router.put()
def rsrc_update():
    pass
@smt_router.delete()
def rsrc_delete():
    pass
