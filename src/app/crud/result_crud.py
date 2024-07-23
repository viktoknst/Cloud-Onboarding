from pymongo.database import Database

from app.models.result import Result


def create(db: Database, id: str):
    db['results'].insert_one(
        {
        'id': id,
        'status': 'running'
        }
    )


def read(db: Database, id: str) -> Result:
    return db['results'].find_one(
        {
            'id': id
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


def delete(db: Database, id: str):
    db['results'].delete_one(
        {
            'id': id
        }
    )
