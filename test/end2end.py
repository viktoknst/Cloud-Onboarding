import requests

SERVER_URL = "http://localhost:3000"
JOHN_DOE_ID = None
JOHN_DOE_ENDPOINT = None

PROJECTS = {}
PROJECT_ID = None

def setup():
    pass

def cleanup():
    pass

#public
def create_user(name):
    endpoint = requests.get(SERVER_URL+"/").json()["create_user"]
    responce = requests.post(SERVER_URL+endpoint, json={"user_name":"john_doe"})
    assert responce.status_code == 200
    #JOHN_DOE_ID = responce.json()["id"]

#public
def log_in(name):
    endpoint = requests.get(SERVER_URL+"/").json()["log_in"]
    responce = requests.get(SERVER_URL+endpoint, json={"user_name":"john_doe"})
    assert responce.status_code == 200
    JOHN_DOE_ID = responce.json()["id"]

#pirvate
def get_user(id):
    endpoint = requests.get(SERVER_URL+"/").json()["user"]
    responce = requests.get(SERVER_URL+endpoint, json={"id":JOHN_DOE_ID})
    assert responce.status_code == 200
    JOHN_DOE_ENDPOINT = responce.json()['endpoint']

#private
def rename_user(id, new_name):
    endpoint = requests.get(SERVER_URL+"/").json()["user"]
    responce = requests.put(SERVER_URL+endpoint, json={"id":JOHN_DOE_ID, "user_name": "jane_doe"})
    assert responce.status_code == 200

#private
def create_project(id):
    endpoint = requests.get(SERVER_URL+"/").json()["create_project"]
    responce = requests.get(SERVER_URL+endpoint, json={"user_id":JOHN_DOE_ID, "project_name": "my_project"})
    assert responce.status_code == 200
    PROJECT_ID = responce.json()['id']

#private
def find_project(id, project_name):
    pass # TODO

#private
def get_project(user_id):
    endpoint = requests.get(SERVER_URL+"/").json()["project"]
    responce = requests.get(SERVER_URL+endpoint, json={"user_id":JOHN_DOE_ID, "project_name": "my_project"})
    assert responce.status_code == 200
    PROJECT_ID = responce.json()['id']

#private
def rename_project(id, new_name):
    pass # TODO

#private
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

#private
def delete_instance(user_id, instance_id):
    pass
