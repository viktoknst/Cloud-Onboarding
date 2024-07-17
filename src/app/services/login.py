from pymongo.database import Database
from typing_extensions import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


def login(db: Database, username: str) -> str | None:
    result = db['users'].find_one(username)
    if result == None:
        return None
    return result['id']
