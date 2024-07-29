from fastapi import APIRouter, HTTPException, Depends

from app.special.config import ENDPOINTS
from app.crud import project_crud, result_crud
from app.external_dependencies.db_interface import DBProxy
#from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectUpdate
import app.services.containerizer.project as project_service
from app.routers.login import get_user_dependency
project_router = APIRouter()


@project_router.post(ENDPOINTS['project']+'/{project_name}')
def create_project(project_name: str, user: User = Depends(get_user_dependency)):
    '''
    s.e.
    '''
    db = DBProxy.get_instance().get_db()
    result = project_crud.create(db, user.id, project_name)
    return {'msg': 'Project created', 'project_id': result}

@project_router.get(ENDPOINTS['project']+'/{project_name}')
def read_project(project_name: str):
    '''
    Endpoint for reading project.
    '''
    db = DBProxy.get_instance().get_db()
    project = project_crud.read(db, project_name)
    return project

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

@project_router.delete(ENDPOINTS['project']+'/{project_name}')
def delete_project(project_name: str):
    '''
    Endpoint for deleting project from db.
    '''
    db = DBProxy.get_instance().get_db()
    project_crud.delete(db, project_name=project_name)
    return {'msg': 'Project deleted'}


# The bellow code is not CRUD
@project_router.post('/run/{project_id}')
def run_project(project_id: str):
    '''
    Endpoint for running project. 
    '''
    db = DBProxy.get_instance().get_db()
    project = project_crud.read(db, project_id)

    result_id = project_service.create_detached_instance(project, db)
    return result_id

@project_router.get('/result/{result_id}')
def get_result(result_id: str):
    '''
    Returns result object.
    '''
    db = DBProxy.get_instance().get_db()
    return result_crud.read(db, result_id)
