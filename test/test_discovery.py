from context import app
import pytest

import app.routers.discovery as discovery
import app.special.config

def test_get_discovery():
    assert discovery.get_discovery() == app.special.config.ENDPOINTS
