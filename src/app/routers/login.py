# TODO: export login logic to a service script, like auth_utils

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer #, OAuth2PasswordRequestForm
from typing_extensions import Annotated

from app.external_dependencies.db_interface import DBProxy
from pymongo.database import Database
from app.services import auth_utils
from app.schemas.login import *

login_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


# may or may not be vulnerable to timing attacks...
@login_router.post("/token")
async def login(r: LoginSchema):
    db: Database = DBProxy.get_instance().get_db()
    user = db['users'].find_one({'name': r.user_name})
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = auth_utils.hash_password(r.password, r.user_name)
    if not hashed_password == user['hashed_password']:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = auth_utils.gen_auth_token(user['name'])
    return {"access_token": token, "token_type": "bearer"}
