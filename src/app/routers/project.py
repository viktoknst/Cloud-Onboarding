from fastapi import APIRouter, HTTPException #, Depends

from app.special.config import ENDPOINTS
from app.crud import project_crud
from app.external_dependencies.db_interface import DBProxy
#from app.models.project import Project
from app.schemas.project import ProjectRunRequest, ProjectCreate, ProjectUpdate
import app.services.containerizer.project as project_service

project_router = APIRouter()


@project_router.post(ENDPOINTS['project'])
def create_project(p: ProjectCreate):
    '''
    s.e.
    '''
    db = DBProxy.get_instance().get_db()
    result = project_crud.create(db, p.user_id, p.project_name)
    if result is not None:
        raise HTTPException(409, result)
    return {'msg': 'Project created'}

# TODO
#@project_router.get(ENDPOINTS['project'])
#def read_project(p: ProjectCreate):
#    db = DBProxy.get_instance().get_db()
#    # project_crud.read(db, )
#    pass

@project_router.put(ENDPOINTS['project'])
def update_project(r: ProjectUpdate):
    db = DBProxy.get_instance().get_db()
    project = project_crud.read(db, r.project_id)

    file_location = f"files/{r.file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    r

# TODO
#@project_router.delete(ENDPOINTS['project'])
#def delete_project():
#    pass


#          NOT CRUD \/ \/ \/

@project_router.post(ENDPOINTS['project'])
def post_run_project(r: ProjectRunRequest):
    '''
    Endpoint for running project. 
    '''
    db = DBProxy.get_instance().get_db()
    project = project_crud.read(db, r.project_id)

    result_id = project_service.create_detached_instance(project, db)
    return result_id
