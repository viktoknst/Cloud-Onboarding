from context import client

from app.special import config

def test_get_discovery():
    '''
    Test discovery endpoint
    '''
    assert client.get('/').json() == config.ENDPOINTS
