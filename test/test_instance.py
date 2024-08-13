import context 

import pytest
from unittest.mock import patch
import time

from app.services.containerizer import *

class DummyContainer:
    def __init__(self):
        pass
    def start(self):
        print('Started')
    def wait(self):
        print('waiting')
    def logs(self):
        return self
    def decode(self):
        return "Hello World!"

def dummy_uuid():
    return 'abc-123'

def assert_insertion(res):
    assert res == {'uuid': 'abc-123', 'status': 'running'}
    print('assertion 1 passed')

def assert_update(resa, resb):
    assert resa == {'uuid': 'abc-123'}
    assert resb == {'$set': {'status': 'done', 'result': 'Hello World!'}}
    print('assertion 2 passed')

@pytest.mark.skip(reason="N/A")
def test_project_instance():
    with patch('src.db_interface.results.insert_one', new=assert_insertion), patch('src.db_interface.results.update_one', new=assert_update), patch('uuid.uuid4', new=dummy_uuid):
        inst = ProjectInstance(DummyContainer())
        print('Running instance in main thread:')
        inst.run()

        print('Running instance in separate thread:')
        inst.start()

        inst2 = ProjectInstance(DummyContainer())

        print('Separate thread:')
        inst2.start()

#if __name__ == "__main__":
#    test_project_instance()
#    print('main exiting... (for real this time)')
