from fastapi import APIRouter, HTTPException, Depends, UploadFile, BackgroundTasks
from typing import Optional

from app.special.config import ENDPOINTS
from app.crud.project_crud import Project
from app.crud.result_crud import Result
from app.crud.user_crud import User
import app.services.containerizer.project as project_service
from app.routers.login import get_user_dependency

project_router = APIRouter()


def get_project(user: User, project_name: str) -> Project:
    try:
        return Project.read(user, name=project_name)
    except Exception as ex:
        raise HTTPException(404, detail='Project not found') from ex


@project_router.post(ENDPOINTS['project']+'/{project_name}')
def create_project(project_name: str, user: User = Depends(get_user_dependency)):
    '''
    s.e.
    '''
    try:
        project = Project.create(user, project_name)
    except Exception as ex:
        raise HTTPException(409, 'Failed to create project') from ex
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
        file_upload: UploadFile,
        is_entry: Optional[bool] = None,
        user: User = Depends(get_user_dependency)
    ):
    '''
    Upload code to project
    '''
    project = get_project(user, project_name)
    project.add_file(file_upload.file, file_upload.filename, bool(is_entry))
    return {'Uploaded file to project'}


@project_router.post('/run/{project_name}')
def run_project(project_name: str, task: BackgroundTasks, user: User = Depends(get_user_dependency)):
    '''
    Endpoint for running project. 
    '''
    project = get_project(user, project_name)
    instance = project_service.create_detached_instance(project)
    task.add_task(instance.run)
    return {'id': instance.result.id}


@project_router.get('/result/{result_id}')
def get_result(result_id: str):
    '''
    Returns result object.
    '''
    return Result.read(id=result_id)
