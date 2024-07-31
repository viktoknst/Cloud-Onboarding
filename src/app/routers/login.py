'''
Login router. For security and authorization.
'''
# TODO move auth dependency to auth_utils instead

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer #, OAuth2PasswordRequestForm

from app.crud.user_crud import User
from app.external_dependencies.db_interface import DBProxy
from app.schemas.login import LoginSchema
from app.services import auth_utils

login_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

User.set_db(DBProxy.get_instance().get_db())

@login_router.post("/token")
async def token_endpoint(r: LoginSchema):
    '''
    Endpoint which takes the user's password and username and returns a JWT. Forward for auth_utils
    '''
    # may or may not be vulnerable to timing attacks... TODO
    try:
        user = User.read(name = r.user_name)
    except Exception as ex:
        raise HTTPException(status_code=400, detail="Incorrect username or password") from ex

    hashed_password = auth_utils.hash_password(r.password, user.salt)

    if hashed_password != user.password_hash:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = auth_utils.gen_auth_token(user.name)
    return {"access_token": token, "token_type": "bearer"}


def verify_token(token: str):
    '''
    Decrypts a token and checks if its valid
    Returns:
        Returns the decrypted token
    '''
    status, decrypted_token = auth_utils.validate_auth_token(token)
    if status != 'OK':
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return decrypted_token


#def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
#    return {"token": token}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    '''
    Dependency for token auth.
    Either takes a token and validates it, returning the user name, or goes to oauth2
    '''
    status, token = auth_utils.validate_auth_token(token)
    if status != 'OK':
        raise HTTPException(403)
    return token['payload']['sub']


async def get_user_dependency(user_name: str = Depends(get_current_user)) -> User:
    '''
    Dependency for token auth.
    Either takes a token and validates it, returning the user dict, or goes to oauth2
    '''
    return User.read(name = user_name)


@login_router.get("/secure-endpoint")
async def secure_endpoint(current_user: str = Depends(get_current_user)):
    '''
    Example secure endpoint with security dependency.
    '''
    return {"message": "Welcome to the secure endpoint", "user": current_user}
