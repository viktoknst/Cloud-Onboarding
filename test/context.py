'''
File to be included in all tests. Does path magic to simulate running from main.py.
Includes pytest and relevant fixtures/handys.
'''

import os
import sys
import mock
import pytest
import mongomock

from fastapi.testclient import TestClient

# black magic that makes the test workdir test/../src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


class MockDBProxy:
    '''
    singleton which holds the db; unnescessary as mongoclient is threadsafe but thats not stopping me
    '''
    __instance = None

    def __init__(self):
        self.client = mongomock.MongoClient()


    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = MockDBProxy()
        return cls.__instance


    def get_db(self):
        return self.client['cob_db']


with mock.patch('app.external_dependencies.db_interface.DBProxy.get_instance', new=MockDBProxy.get_instance):
    import main
    client = TestClient(main.app)


def does_nothing(*args):
    '''
    Does nothing. Use for tests.
    '''


def always_false(*args):
    return False


def always_true(*args):
    return True


def always_excepts(*args):
    raise Exception('A testing exception')


@pytest.fixture
def get_mock_db() -> mongomock.Database:
    '''
    Fixture for getting a non-persistant mongo db
    '''
    return MockDBProxy.get_instance().get_db()

@pytest.fixture
def get_test_user(get_mock_db) -> any:
    '''
    Creates testing user.
    Returns header to be used for the newly created user.
    Cleans up after.
    '''
    with mock.patch('os.mkdir', new=does_nothing), mock.patch('os.path.exists', new=always_false):
        responce = client.post(
                '/user',
                json={
                    'user_name': 'John Doe',
                    'password': 'password1234'}
            )
        assert responce.status_code == 200

    result = client.post(
        '/token',
        json={
            'user_name': 'John Doe',
            'password': 'password1234'}
        )
    assert responce.status_code == 200

    token = result.json()['access_token']
    auth_header = {"Authorization": f"Bearer {token}"}

    yield auth_header

    with mock.patch('os.path.exists', new=always_true), mock.patch('shutil.rmtree', new=does_nothing):
        result = client.delete(
            '/user',
            headers=auth_header
        )
