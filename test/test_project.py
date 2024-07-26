import context
from context import client
from unittest import mock

class TestProject():
    @mock.patch('app.external_dependencies.db_interface.DBProxy', new=context.MockDBProxy)
    def test_create(self):
        responce = client.post('/project', json={'user_id':'abc', 'project_name':'project'})
        assert responce.status_code == 409
        context.MockDBProxy.get_instance().get_db()['users'].insert_one({'id':'abc', 'dir':'~/testing'})
        responce = client.post('/project', json={'user_id':'abc', 'project_name':'project'})
        assert responce.status_code == 200

    def test_update(self):
        pass

    def test_run(self):
        pass

if __name__ == '__main__':
    a = TestProject()
    a.test_create()