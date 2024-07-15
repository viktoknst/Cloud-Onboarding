from fastapi import FastAPI

from src.app.routers import *

app = FastAPI()

app.include_router(discovery_router)
app.include_router(project_router)
app.include_router(user_router)
