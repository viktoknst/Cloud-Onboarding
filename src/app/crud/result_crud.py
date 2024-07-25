"""
Module that handles CRUD operations for results in the DB
"""

from pymongo.database import Database

from app.models.result import Result


def create(mongo_db: Database, result_id: str) -> None:
    """
        Creates result into the given DB.
        Result is created as 'running' by default

    Args:
        db (Database): _description_
        id (str): _description_
    """
    mongo_db['results'].insert_one(
        {
        'id': result_id,
        'status': 'running'
        }
    )


def read(mongo_db: Database, result_id: str) -> Result:
    """
        Reads given result from the given DB.
    
    Args:
        db (Database): _description_
        result_id (str): _description_

    Returns:
        Result: _description_
    """
    return mongo_db['results'].find_one(
        {
            'id': result_id
        }
    )


def update(db: Database, r: Result):
    
    db['results'].update_one(
    {
        'uuid': r.id
    },
    {'$set':
        {
            'status': 'done',
            'result': r.result
        }
    }
    )


def delete(db: Database, result_id: str):
    db['results'].delete_one(
        {
            'id': result_id
        }
    )
