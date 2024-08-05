'''
FastAPI App entrypoint. This is the file to be ran with 'fastapi run'
Endpoints will not be used by server unless added to `app`
'''

from fastapi import FastAPI

from app.routers.discovery import discovery_router
from app.routers.login import login_router
from app.routers.project import project_router
from app.routers.user import user_router

from app.external_dependencies.db_interface import DBProxy

from app.crud.project_crud import Project
from app.crud.user_crud import User
from app.crud.result_crud import Result

DB_CLIENT = DBProxy.get_instance()
Project.set_db(DB_CLIENT.get_db())
User.set_db(DB_CLIENT.get_db())
Result.set_db(DB_CLIENT.get_db())

app = FastAPI()

app.include_router(discovery_router)
app.include_router(login_router)
app.include_router(project_router)
app.include_router(user_router)
