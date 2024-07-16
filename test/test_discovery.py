from context import src
import pytest

import src.api.discovery as discovery
import app.special.config

def test_get_discovery():
    assert discovery.get_discovery() == app.special.config.ENDPOINTS
