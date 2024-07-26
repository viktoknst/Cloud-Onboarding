'''
File to be included in all tests. Does path magic to simulate running from main.py.
Includes pytest and relevant fixtures/handys.
'''

# include in all tests:
#
#from context import src
#from context import config
#
#import pytest
#from unittest.mock import patch
#
#from src import myfile

import os
import sys
import pytest
import mongomock
from fastapi.testclient import TestClient

# black magic that makes the test workdir test/../src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import main
client = TestClient(main.app)

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

@pytest.fixture
def get_mock_db() -> mongomock.Database:
    '''
    Fixture for getting a non-persistant mongo db
    '''
    return MockDBProxy.get_instance().get_db()
