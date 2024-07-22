from fastapi import APIRouter, HTTPException, Depends
from app.special.config import ENDPOINTS

import app.crud.project_crud as project_crud
from app.external_dependencies.db_interface import DBProxy
from app.models.project import Project
from app.schemas.project import *
from app.services.containerizer import project
import app.services.containerizer.project as project_service

project_router = APIRouter()


@project_router.post(ENDPOINTS['project'])
def create_project(p: ProjectCreate):
    db = DBProxy.get_instance().get_db()
    result = project_crud.create(db, p.user_id, p.project_name)
    if result!= None:
        raise HTTPException(409, result)
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


#          NOT CRUD \/ \/ \/


@project_router.post(ENDPOINTS['project'])
def post_run_project(r: ProjectRunRequest):
    #if re.match(r'^[a-zA-Z0-9_-]{4,16}$', p.project_name) == None:
    #    raise HTTPException(409, "Project name is invalid")
    #if os.path.exists(USER_DB['user_dir']+'/'+get_user().user_name+'/'+p.project_name):
    #    raise HTTPException(409, "Project name is in use!")
    #os.mkdir(USER_DB['user_dir']+"/"+get_user().user_name+'/'+p.project_name)
    #return {'msg': 'Project created'}
    project = Project(r.project_id)
    id = project_service.create_detached_instance(Project)
    return id


#@project_router.get(ENDPOINTS['result'])
#def get_result(g: ResultRequest):
#    return
