from fastapi import APIRouter, HTTPException, Depends

from app.special.config import ENDPOINTS
from app.crud.project_crud import Project
from app.crud.result_crud import Result
from app.crud.user_crud import User
from app.external_dependencies.db_interface import DBProxy
#from app.models.project import Project
from app.schemas.project import ProjectUpdate
import app.services.containerizer.project as project_service
from app.routers.login import get_user_dependency

project_router = APIRouter()

User.set_db(DBProxy.get_instance().get_db())
Result.set_db(DBProxy.get_instance().get_db())
Project.set_db(DBProxy.get_instance().get_db())


def get_project(user: User, project_name: str) -> Project:
    try:
        return Project.create(user, project_name)
    except Exception as ex:
        raise HTTPException(404, detail='Project not found') from ex


@project_router.post(ENDPOINTS['project']+'/{project_name}')
def create_project(project_name: str, user: User = Depends(get_user_dependency)):
    '''
    s.e.
    '''
    project = get_project(user, project_name)
    return {'msg': 'Project created', 'project': project.to_jsons()}


@project_router.get(ENDPOINTS['project']+'/{project_name}')
def read_project(project_name: str, user: User = Depends(get_user_dependency)):
    '''
    Endpoint for reading project.
    '''
    project = get_project(user, project_name)
    return {'project':project.to_jsons()}


# NOT IN USE
#@project_router.put(ENDPOINTS['project']+'/{project_name}')
#def update_project():
#    pass


@project_router.delete(ENDPOINTS['project']+'/{project_name}')
def delete_project(project_name: str, user: User = Depends(get_user_dependency)):
    '''
    Endpoint for deleting project from db.
    '''
    project = get_project(user, project_name)
    project.delete()
    return {'msg': 'Project deleted', 'project': project.to_jsons()}


@project_router.put(ENDPOINTS['project']+'/{project_name}/upload')
def upload_code(
        project_name: str,
        file_request: ProjectUpdate,
        user: User = Depends(get_user_dependency)
    ):
    '''
    Upload code to project
    '''
    project = get_project(user, project_name)

    file_location = f"{project.source_dir}/{file_request.file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file_request.file.file.read())
    if file_request.is_entry is True:
        project.entry_file = file_request.file.filename
        project.update()
    return 'Uploaded file to project'


@project_router.post('/run/{project_id}')
def run_project(project_id: str, user: User = Depends(get_user_dependency)):
    '''
    Endpoint for running project. 
    '''

    project = Project.read(user, id=project_id)
    db = DBProxy.get_instance().get_db()
    result_id = project_service.create_detached_instance(project, db)
    return result_id


@project_router.get('/result/{result_id}')
def get_result(result_id: str):
    '''
    Returns result object.
    '''
    return Result.read(id=result_id).to_jsons()
