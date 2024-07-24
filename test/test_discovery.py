from context import app
import pytest

from app.routers import discovery
import app.special.config

def test_get_discovery():
    assert discovery.get_discovery() == app.special.config.ENDPOINTS

