from pymongo.database import Database
from app.models.result import Result


def create(db: Database, id: str):
    db['results'].insert_one(
        {
        'uuid': id,
        'status': 'running'
        }
    )


def read():
    pass


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


def delete():
    pass
