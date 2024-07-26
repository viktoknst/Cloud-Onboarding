from . import context

from app.routers import discovery
from app.special import config

def test_get_discovery():
    assert discovery.get_discovery() == config.ENDPOINTS

