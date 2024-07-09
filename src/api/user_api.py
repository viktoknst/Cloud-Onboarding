from config import ENDPOINTS
from config import USER_DB

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import os
import re

user_router = APIRouter()

class UserCreationRequest(BaseModel):
    user_name: str

@user_router.post(ENDPOINTS['create_user'])
def post_create_user(u: UserCreationRequest):
    if not re.fullmatch(u.user_name, '/^[a-zA-Z0-9_-]{4,16}$/'):
        raise HTTPException(409, "Username is invalid")
    if os.path.exist(USER_DB['user_dir']+"/"+u.user_name):
        raise HTTPException(409, "Username is in use!")
    os.mkdir(USER_DB['user_dir']+"/"+u.user_name)
    return {'msg': 'User created'}
