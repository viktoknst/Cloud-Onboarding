# TODO: export login logic to a service script, like auth_utils
from typing_extensions import Annotated

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2PasswordBearer #, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse

from app.crud import user_crud
from app.external_dependencies.db_interface import DBProxy
from app.schemas.login import *
from app.services import auth_utils

login_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# may or may not be vulnerable to timing attacks...
@login_router.post("/token")
async def token(r: LoginSchema):
    db = DBProxy.get_instance().get_db()
    user = user_crud.read(db, name = r.user_name)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    hashed_password = auth_utils.hash_password(r.password, r.user_name, user.salt)

    if not hashed_password == user.password_hash:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = auth_utils.gen_auth_token(user.name)
    return {"access_token": token, "token_type": "bearer"}


def verify_token(token: str):
    status, decrypted_token = auth_utils.validate_auth_token(token)
    if status != 'OK':
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return decrypted_token


async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        return RedirectResponse(url="/login")
    return verify_token(token)['payload']['sub']


def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@login_router.get("/secure-endpoint")
async def secure_endpoint(current_user: str = Depends(get_current_user)):
    return {"message": "Welcome to the secure endpoint", "user": current_user}
