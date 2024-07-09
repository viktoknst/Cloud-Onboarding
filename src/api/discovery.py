from config import ENDPOINTS

from fastapi import APIRouter

discovery_router = APIRouter()

@discovery_router.get(ENDPOINTS['discovery'])
def get_discovery():
    return ENDPOINTS
