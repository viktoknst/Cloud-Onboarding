"""
Discovery router. File for discovery endpoint.
"""

from fastapi import APIRouter

from app.special.config import ENDPOINTS

discovery_router = APIRouter()

@discovery_router.get(ENDPOINTS['discovery'])
def get_discovery() -> dict:
    """
    Returns a dict of the server's configured endpoints
    """
    return ENDPOINTS
