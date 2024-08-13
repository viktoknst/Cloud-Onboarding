'''
File for testing user endpoints with pytest
'''

from unittest import mock
import pytest
from context import *
import json

@mock.patch('os.mkdir', new=does_nothing)
class TestUser():
    '''
    Tests project-related endpoints
    '''
    @mock.patch('os.path.exists', new=always_false)
    def test_create_fail_user_exists(self, get_test_user):
        '''
        By getting test user (named john doe) we ensure the name is taken
        '''
        responce = client.post(
            '/user',
            json={
                'user_name': 'John Doe',
                'password': 'password1234'}
        )
        assert responce.status_code == 409, responce.status_code # Failed to create user: reason


    @mock.patch('os.path.exists', new=always_false)
    def test_create_fail_bad_username(self):
        responce = client.post(
            '/user',
            json={
                'user_name': '1 @#rTHFGJ',
                'password': 'password1234'}
        )
        assert responce.status_code == 409 # Failed to create user: reason


    @mock.patch('os.path.exists', new=always_false)
    def test_create_succeed(self, get_mock_db):
        get_mock_db.drop_collection('users') # cleanup
        responce = client.post(
            '/user',
            json={
                'user_name': 'John Doe',
                'password': 'password1234'}
        )
        assert responce.status_code == 200 # Now works
        get_mock_db.drop_collection('users') # cleanup


    def test_read(self, get_test_user):
        responce = client.get(
            '/user',
            headers=get_test_user
        )
        assert responce.status_code == 200
        assert json.loads(responce.text)['user']['name'] == 'John Doe'


    def test_update_fail_bad_username(self, get_test_user):
        responce = client.put(
            '/user',
            json={
                'user_name': '1 @#rTHFGJ',
                'password': 'password1234'},
            headers=get_test_user
        )
        assert responce.status_code == 409 # Failed to update user


    def test_update_succeed(self, get_test_user):
        responce = client.put(
            '/user',
            json={
                'user_name': 'Jane Doe',
                'password': 'password4321'},
            headers=get_test_user
        )
        assert responce.status_code == 200
        assert json.loads(responce.text)['user']['name'] == 'Jane Doe'


    @mock.patch('os.path.exists', new=always_true)
    @mock.patch('shutil.rmtree', new=does_nothing)
    def test_delete(self, get_test_user):
        responce = client.delete(
            '/user',
            headers=get_test_user
        )
        assert responce.status_code == 200
