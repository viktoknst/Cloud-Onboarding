'''
FastAPI App entrypoint. This is the file to be ran with 'fastapi run'
'''

from fastapi import FastAPI

from app.routers.discovery import discovery_router
from app.routers.login import login_router
from app.routers.project import project_router
from app.routers.user import user_router

app = FastAPI()

app.include_router(discovery_router)
app.include_router(login_router)
app.include_router(project_router)
app.include_router(user_router)
