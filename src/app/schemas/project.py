from pydantic import BaseModel


class ProjectCreate(BaseModel):
    user_id: str
    project_name: str


class Project(BaseModel):
    user_id: str
    project_name: str


class ProjectRunRequest(BaseModel):
    user_id: str
    project_id: str


class ResultQuery(BaseModel):
    id: str
