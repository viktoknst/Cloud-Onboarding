from fastapi import APIRouter, HTTPException, Depends

from app.special.config import ENDPOINTS
from app.crud import project_crud, result_crud
from app.external_dependencies.db_interface import DBProxy
#from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectRunRequest, ProjectCreate, ProjectUpdate, ResultQuery, ProjectRead
import app.services.containerizer.project as project_service
from app.routers.login import get_user_dependency
project_router = APIRouter()


@project_router.post(ENDPOINTS['project'])
def create_project(p: ProjectCreate, user: User = Depends(get_user_dependency)):
    '''
    s.e.
    '''
    db = DBProxy.get_instance().get_db()
    result = project_crud.create(db, user.id, p.project_name)
    return {'msg': 'Project created', 'project_id': result}

#@project_router.get(ENDPOINTS['project'])
#def read_project(p: ProjectRead):
#    db = DBProxy.get_instance().get_db()
#    project_crud.read(db, )
#    pass

@project_router.put(ENDPOINTS['project'])
def update_project(r: ProjectUpdate):
    '''
    Uploads/updates a file to the project dir.
    '''
    db = DBProxy.get_instance().get_db()
    project = project_crud.read(db, r.project_id)

    file_location = f"{project.source_dir}/{r.file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(r.file.file.read())
    return 'Uploaded file to project'

# TODO
#@project_router.delete(ENDPOINTS['project'])
#def delete_project():
#    pass


#          NOT CRUD \/ \/ \/

@project_router.post('/run')
def run_project(r: ProjectRunRequest):
    '''
    Endpoint for running project. 
    '''
    db = DBProxy.get_instance().get_db()
    project = project_crud.read(db, r.project_id)

    result_id = project_service.create_detached_instance(project, db)
    return result_id

@project_router.get('/result')
def get_result(r: ResultQuery):
    '''
    Returns result object.
    '''
    db = DBProxy.get_instance().get_db()
    return result_crud.read(db, r.result_id)
