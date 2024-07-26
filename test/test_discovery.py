import context
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

from app.special import config

def test_get_discovery():
    '''
    Test discovery endpoint
    '''
    assert client.get('/').json() == config.ENDPOINTS
