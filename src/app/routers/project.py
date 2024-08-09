from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, UploadFile, BackgroundTasks

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
    return {'msg': 'Project created', 'project': project.to_dict()}


@project_router.get(ENDPOINTS['project']+'/{project_name}')
def read_project(project_name: str, user: User = Depends(get_user_dependency)):
    '''
    Endpoint for reading project.
    '''
    project = get_project(user, project_name)
    return {'project':project.to_dict(), 'dir': project.read_file_structure()}


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
    return {'msg': 'Project deleted', 'project': project.to_dict()}


@project_router.put(ENDPOINTS['project']+'/files/{project_name}/{file_path:path}')
def upload_code(
        project_name: str,
        file_path: str,
        file_upload: Optional[UploadFile] = None,
        is_dir: Optional[bool] = None,
        is_entry: Optional[bool] = None,
        user: User = Depends(get_user_dependency)
    ):
    '''
    Upload code to project
    '''
    project = get_project(user, project_name)
    try:
        if is_dir:
            project.add_dir(file_path)
        else:
            project.add_file(file_path, file_upload.file, bool(is_entry))
    except Exception as ex:
        raise HTTPException(400, 'Failed to delete file. Are you sure it exits?') from ex
    return {'msg': 'Uploaded file to project', 'file_path': file_path}


@project_router.delete(ENDPOINTS['project']+'/files/{project_name}/{file_path:path}')
def delete_code(
        project_name: str,
        file_path: str,
        user: User = Depends(get_user_dependency)
    ):
    project = get_project(user, project_name)
    try:
        project.remove_file(file_path)
    except Exception as ex:
        raise HTTPException(404, detail="File/dir not found!") from ex
    return {'Removed file from project'}

# TODO
@project_router.put(ENDPOINTS['project']+'/depends/')
def update_dependencies():
    return {'n/a'}


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
