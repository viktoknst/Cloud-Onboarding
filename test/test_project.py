import context
from context import client
from unittest import mock

def func(*args):
    '''
    Does nothing. Use for tests.
    '''

class TestProject():
    @mock.patch('os.mkdir', new=func)
    @mock.patch('app.external_dependencies.db_interface.DBProxy.get_instance', new=context.MockDBProxy.get_instance)
    def test_create(self):
        responce = client.post('/project', json={'user_id':'abc', 'project_name':'project'})
        assert responce.status_code == 409 # User abd doesnt exist
        # create user abc
        context.MockDBProxy.get_instance().get_db()['users'].insert_one({'id':'abc', 'dir':''})
        responce = client.post('/project', json={'user_id':'abc', 'project_name':'project'})
        assert responce.status_code == 200 # Now works

    def test_update(self):
        pass

    def test_run(self):
        pass

if __name__ == '__main__':
    a = TestProject()
    a.test_create()
