from fastapi import APIRouter

from src.config import ENDPOINTS

discovery_router = APIRouter()

@discovery_router.get(ENDPOINTS['discovery'])
def get_discovery():
    return ENDPOINTS
