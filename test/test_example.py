'''
File to ensure that tests are working properly.
'''

import context
import pytest

from app.special import test


def test_add_two_nums():
    '''
    Used for testing
    '''
    assert test.add_two_nums(1,2) == 3
    assert test.add_two_nums(6,-8.5) == -2.5
    with pytest.raises(Exception): # assert an exception is raised
        assert test.add_two_nums(1,2) == 4
    with pytest.raises(Exception):
        test.add_two_nums("Helo", None)

#@pytest.fixture
#def mongo_collection(monkeypatch):
#    # Mock the MongoClient to use mongomock
#    mock_client = mongomock.MongoClient()
#    mock_db = mock_client['mydatabase']
#    mock_collection = mock_db['mycollection']
#    monkeypatch.setattr('myapp.db.get_collection', lambda: mock_collection)
#    return mock_collection

#def test_insert_document(mongo_collection):
#    doc = {'name': 'test', 'value': 123}
#    doc_id = insert_document(doc)
#    inserted_doc = mongo_collection.find_one({'_id': doc_id})
#    assert inserted_doc is not None
#    assert inserted_doc['name'] == 'test'
#    assert inserted_doc['value'] == 123

#def test_find_document(mongo_collection):
#    doc = {'name': 'findme', 'value': 456}
