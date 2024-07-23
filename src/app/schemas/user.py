from pydantic import BaseModel


class UserCreate(BaseModel):
    user_name: str
    password: str


class UserRead(BaseModel):
    id: str


class UserDelete(BaseModel):
    id: str


class User(BaseModel):
    id: str
    user_name: str


class UpdateUser(BaseModel):
    id: str | None