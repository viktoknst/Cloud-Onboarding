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
# black magic that makes the test workdir test/../src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pytest
import mongomock


# TODO: implement mongomock monkeypatching
@pytest.fixture
def mongo_collection(monkeypatch):
    # Mock the MongoClient to use mongomock
    mock_client = mongomock.MongoClient()
    mock_db = mock_client['mydatabase']
    mock_collection = mock_db['mycollection']
    monkeypatch.setattr('myapp.db.get_collection', lambda: mock_collection)
    return mock_collection

import app.special.config as config
import app
