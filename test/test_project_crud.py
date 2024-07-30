'''
n/a
'''

import context

from app.crud import project_crud

class TestProjectCrud:
    """
    s.e.
    """
    def test_create():
        pass
    def test_read():
        pass
    def test_update():
        pass
    def test_delete():
        pass

import mongomock
import pytest

@pytest.fixture
def mongo_collection(monkeypatch):
    # Mock the MongoClient to use mongomock
    mock_client = mongomock.MongoClient()
    mock_db = mock_client['mydatabase']
    mock_collection = mock_db['mycollection']
    monkeypatch.setattr('myapp.db.get_collection', lambda: mock_collection)
    return mock_collection

def test_insert_document(mongo_collection):
    doc = {'name': 'test', 'value': 123}
    doc_id = insert_document(doc)
    inserted_doc = mongo_collection.find_one({'_id': doc_id})
    assert inserted_doc is not None
    assert inserted_doc['name'] == 'test'
    assert inserted_doc['value'] == 123

def test_find_document(mongo_collection):
    doc = {'name': 'findme', 'value': 456}
