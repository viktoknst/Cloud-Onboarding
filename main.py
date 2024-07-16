from fastapi import FastAPI

from src.app.routers.discovery import discovery_router
#from src.app.routers.project import project_router
#from src.app.routers.user import user_router

app = FastAPI()

app.include_router(discovery_router)
#app.include_router(project_router)
#app.include_router(user_router)
