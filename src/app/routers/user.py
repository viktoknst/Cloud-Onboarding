from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.config import ENDPOINTS

from app.schemas.user import *

user_router = APIRouter()


@user_router.post(ENDPOINTS['create_user'])
def create_user(u: UserCreate):
    pass


@user_router.get()
def read_user():
    pass


@user_router.put()
def update_user():
    pass


@user_router.delete()
def delete_user():
    pass
