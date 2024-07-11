from ..config import ENDPOINTS
from ..config import USER_DB

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import os
import re

project_router = APIRouter()

def get_user():
    pass

class ProjectCreationRequest(BaseModel):
    project_name: str

@project_router.post(ENDPOINTS['project'])
def post_create_project(p: ProjectCreationRequest):
    if re.match(r'^[a-zA-Z0-9_-]{4,16}$', p.project_name) == None:
        raise HTTPException(409, "Project name is invalid")
    if os.path.exists(USER_DB['user_dir']+'/'+get_user().user_name+'/'+p.project_name):
        raise HTTPException(409, "Project name is in use!")
    os.mkdir(USER_DB['user_dir']+"/"+get_user().user_name+'/'+p.project_name)
    return {'msg': 'Project created'}




# -----------------------------------------------------------------------------------------------
#private
def create_project(id):
    endpoint = requests.get(SERVER_URL+"/").json()["create_project"]
    responce = requests.get(SERVER_URL+endpoint, json={"user_id":JOHN_DOE_ID, "project_name": "my_project"})
    assert responce.status_code == 200
    PROJECT_ID = responce.json()['id']


def run_project(user_id, project_id):
    endpoint = requests.get(SERVER_URL+"/"+"?run=yes").json()["project"]
    responce = requests.put(SERVER_URL+endpoint, json={"user_id":JOHN_DOE_ID, "project_id": PROJECT_ID})
    assert responce.status_code == 200
    instance_id = responce.json()['id']

#private #NOTE an instance has at best a spiritual bond with its projects. for our purposes they are independent
def get_instances(user_id, name):
    pass

#private
def get_instance_result(user_id, instance_id):
    endpoint = requests.get(SERVER_URL+"/").json()["project"]
    responce = requests.put(SERVER_URL+endpoint, json={"user_id":JOHN_DOE_ID, "project_id": PROJECT_ID})
    assert responce.status_code == 200
    result = responce.json()['result']
    print(result)
