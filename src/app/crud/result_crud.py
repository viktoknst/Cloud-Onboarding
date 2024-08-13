"""
Module that handles CRUD operations for results in the DB
"""
import uuid

from pymongo.database import Database

class Result:
    """
    Object representation of the result from running a project.
    Handles saving/reading from a db.
    """

    db: Database

    @classmethod
    def set_db(cls, db: Database):
        """Sets the database to be used by the class and all its instances.

        Args:
            db (Database): A mongo-like db
        """
        cls.db = db


    def __init__(self, id: str, status: str, result: str):
        self.id = id
        self.status = status
        self.result = result


    @classmethod
    def create(cls, result: str | None):
        """
            Creates result into the given DB.
            Result is created as 'running' by default

        Args:
            db (Database): _description_
            id (str): _description_
        """
        id = str(uuid.uuid4())

        if result is None:
            status = 'running'
        else:
            status = 'done'

        cls.db['results'].insert_one(
            {
                'id': id,
                'status': status,
                'result': result
            }
        )

        return Result(id, status, result)


    @classmethod
    def read(cls, id: str):
        """
            Reads given result from the given DB.
        
        Args:
            db (Database): _description_
            result_id (str): _description_
    
        Returns:
            Result: _description_
        """
        result = cls.db['results'].find_one(
            {
                'id': id
            }
        )
        if result is None:
            raise ValueError('Result id does not exist')
        return Result(
            result['id'],
            result['status'],
            result['result'],
        )


    def update(self) -> None:
        """
        Saves the current state of the object (fields) to the db.
        Some fields that should not be altered are not saved.
        """
        self.db['results'].update_one(
            {
                'id': self.id
            },
            {'$set':
                {
                    'status': self.status,
                    'result': self.result
                }
            }
        )


    def delete(self) -> None:
        self.db['results'].delete_one(
            {
                'id': self.id
            }
        )


    def to_dict(self):
        return{
            'id': self.id,
            'result': self.result
        }
