import context

from fastapi.testclient import TestClient

from app.special import config
import main

client = TestClient(main.app)

def test_get_discovery():
    '''
    Test discovery endpoint
    '''
    assert client.get('/').json() == config.ENDPOINTS

