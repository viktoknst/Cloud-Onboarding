'''
File for testing project endpoints with pytest
'''

from context import *
from unittest import mock
import pytest
from time import sleep

@mock.patch('os.mkdir', new=does_nothing)
class TestProject():
    '''
    Tests project-related endpoints
    '''
    @mock.patch('os.path.exists', new=always_true)
    def test_create_fail_project_exists(self, get_test_user):
        responce = client.post(
            '/project/myproject',
            headers=get_test_user
        )
        assert responce.status_code == 409 # User abc doesnt exist


    @mock.patch('os.path.exists', new=always_false)
    def test_create_succeed(self, get_test_user, get_mock_db):
        responce = client.post(
            '/project/myproject',
            headers=get_test_user
        )
        assert responce.status_code == 200 # Now works
        get_mock_db.drop_collection('users')

    @pytest.mark.skip(reason="Not in use")
    @mock.patch('os.path.exists', new=always_true)
    def test_update(self, get_test_user):
        responce = client.post(
            '/project/myproject',
            headers=get_test_user
        )
        assert responce.status_code == 200


    @mock.patch('os.path.exists', new=always_false)
    @pytest.mark.skip(reason="Requires file opperations")
    def test_upload(self, get_test_user):
        response = client.post(
            '/project/myproject',
            headers=get_test_user
        )
        assert response.status_code == 200
        with open('test/hello_world.py', 'rb+') as file:
            response = client.put(
                "/project/myproject/upload?is_entry=yes",
                files={"file": ('hello_world.py', file, "text/plain")},
                headers=get_test_user
            )
        assert response.status_code == 200


    def test_run_and_get_result(self, get_test_project, get_mock_db):
        response = client.post(
            '/run/myproject',
            headers=get_test_project
        )
        assert response.status_code == 200
        result_id = response.json()['id']
        response = client.get(
                f'/result/{result_id}'
        )
        while(response.json()['status'] == 'running'):
            response = client.get(
                f'/result/{result_id}'
            )
            sleep(1)
        assert response.status_code == 200
        assert response.json()['result'] == 'Hello world!\n'

#if __name__ == "__main__":
#    for i in get_test_user(get_mock_db()):
#        user = i
#    TestProject.test_run_and_get_result(None, user)