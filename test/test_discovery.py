from context import src
import pytest

import src.api.discovery as discovery
import src.config

def test_get_discovery():
    assert discovery.get_discovery() == src.config.ENDPOINTS
