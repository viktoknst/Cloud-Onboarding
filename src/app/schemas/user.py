from pydantic import BaseModel


class UserCreate(BaseModel):
    user_name: str


class User(BaseModel):
    user_name: str
