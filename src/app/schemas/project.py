from fastapi import UploadFile
from pydantic import BaseModel

class ProjectCreate(BaseModel):
    project_name: str


class ProjectRead(BaseModel):
    project_name: str


class ProjectRunRequest(BaseModel):
    user_id: str
    project_id: str


class ResultQuery(BaseModel):
    result_id: str

class ProjectUpdate(BaseModel):
    user_id: str
    project_id: str
    file: UploadFile