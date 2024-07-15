from fastapi import APIRouter, HTTPException

from config import ENDPOINTS

from app.external_dependencies.db_interface import DBProxy
from app.models.project import Project
from app.schemas.project import *
from app.services.containerizer import project


project_router = APIRouter()



@project_router.post(ENDPOINTS['project'])
def create_project(p: ProjectCreationRequest):
    if re.match(r'^[a-zA-Z0-9_-]{4,16}$', p.project_name) == None:
        raise HTTPException(409, "Project name is invalid")
    if os.path.exists(USER_DB['user_dir']+'/'+get_user(p.user_id)+'/'+p.project_name):
        raise HTTPException(409, "Project name is in use!")
    os.mkdir(USER_DB['user_dir']+"/"+get_user(p.user_id)+'/'+p.project_name)
    return {'msg': 'Project created'}


@project_router.get(ENDPOINTS['project'])
def read_project():
    pass


@project_router.put(ENDPOINTS['project'])
def update_project():
    pass


@project_router.delete(ENDPOINTS['project'])
def delete_project():
    pass


@project_router.post(ENDPOINTS['project'])
def post_run_project(r: ProjectRunRequest):
    #if re.match(r'^[a-zA-Z0-9_-]{4,16}$', p.project_name) == None:
    #    raise HTTPException(409, "Project name is invalid")
    #if os.path.exists(USER_DB['user_dir']+'/'+get_user().user_name+'/'+p.project_name):
    #    raise HTTPException(409, "Project name is in use!")
    #os.mkdir(USER_DB['user_dir']+"/"+get_user().user_name+'/'+p.project_name)
    #return {'msg': 'Project created'}
    project = Project(r.project_id)
    id = Project.create_detached_instance()
    return id


@project_router.get(ENDPOINTS['result'])
def get_result(g: ResultRequest):
    return
