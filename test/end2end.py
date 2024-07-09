import requests

SERVER_URL = "http://localhost:3000"
JOHN_DOE_ID = None
JOHN_DOE_ENDPOINT = None
PROJECTS = {}

def setup():
    pass

def cleanup():
    pass

def create_user(name):
    endpoint = requests.get(SERVER_URL+"/").json()["create_user"]
    responce = requests.post(SERVER_URL+endpoint, json={"user_name":"john_doe"})
    assert responce.status_code == 200
    #JOHN_DOE_ID = responce.json()["id"]

def log_in(name):
    endpoint = requests.get(SERVER_URL+"/").json()["log_in"]
    responce = requests.get(SERVER_URL+endpoint, json={"user_name":"john_doe"})
    assert responce.status_code == 200
    JOHN_DOE_ID = responce.json()["id"]

def get_user_endpoint(id):
    endpoint = requests.get(SERVER_URL+"/").json()["get_user"]
    responce = requests.get(SERVER_URL+endpoint, json={"id":JOHN_DOE_ID})
    assert responce.status_code == 200
    JOHN_DOE_ENDPOINT = responce.json()['endpoint']

def create_project(id):
    endpoint = requests.get(SERVER_URL+"/").json()["create_project"]
    responce = requests.get(SERVER_URL+endpoint, json={"user_id":JOHN_DOE_ID, "project_name": "my_project"})
    assert responce.status_code == 200
    PROJECT_ID = responce.json()['id']

def rename_user(id, new_name):
    endpoint = requests.get(SERVER_URL+"/").json()["get_user"]
    responce = requests.put(SERVER_URL+endpoint, json={"id":JOHN_DOE_ID, "user_name": "jane_doe"})
    assert responce.status_code == 200

def rename_project(id, new_name):
    pass # TODO
