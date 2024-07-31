'''
File for testing project endpoints with pytest
'''

from context import *
from unittest import mock
import pytest


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
    def test_create_succeed(self, get_test_user):
        responce = client.post(
            '/project/myproject',
            headers=get_test_user
        )
        assert responce.status_code == 200 # Now works


    @pytest.mark.skip(reason="Not in use")
    @mock.patch('os.path.exists', new=always_true)
    def test_update(self, get_test_user):
        responce = client.post(
            '/project/myproject',
            headers=get_test_user
        )
        assert responce.status_code == 200


    @mock.patch('os.path.exists', new=always_false)
    def test_upload(self, get_test_user):
        response = client.post(
            '/project/myproject',
            headers=get_test_user
        )
        assert response.status_code == 200
        with open('test/hello_world.py', 'rb+') as file:
            response = client.put(
                "/project/myproject/upload",
                files={"file": ('hello_world.py', file, "text/plain")},
                headers=get_test_user
            )
        print(response)
        assert response.status_code == 200

    #TODO
    @pytest.mark.skip(reason="Functionality not implemented")
    def test_run(self):
        pass
