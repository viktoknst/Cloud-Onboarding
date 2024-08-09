'''
File to be included in all tests. Does path magic to simulate running from main.py.
Includes pytest and relevant fixtures/handys.
'''

import os
import sys
import mock
import pytest
import mongomock
import shutil

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
    responce = client.post(
            '/user',
            json={
                'user_name': 'John Doe',
                'password': 'password1234'}
        )
    assert responce.status_code == 200

    responce = client.post(
        '/token',
        json={
            'user_name': 'John Doe',
            'password': 'password1234'}
        )
    assert responce.status_code == 200

    token = responce.json()['access_token']
    auth_header = {"Authorization": f"Bearer {token}"}

    yield auth_header

    if os.path.exists('users/John Doe'):
        shutil.rmtree('users/John Doe')
    get_mock_db.drop_collection('users')

@pytest.fixture
def get_test_project(get_test_user, get_mock_db) -> any:
    responce = client.post(
        '/project/myproject',
        headers=get_test_user
    )
    assert responce.status_code == 200, responce.text
    with open('test/hello_world.py', 'rb+') as file:
        response = client.put(
            "/project/files/myproject/hello_world.py",
            files={"file_upload": ('hello_world.py', file, "text/plain")},
            headers=get_test_user,
            params={'is_entry': True}
        )
    assert response.status_code == 200, response.text

    yield get_test_user
    if os.path.exists('users/John Doe/myproject'):
        shutil.rmtree('users/John Doe/myproject')
    get_mock_db.drop_collection('projects')
