from pymongo.database import Database

class User:
    id: str
    name: str


    def __init__(self, id, name):
        self.id = id
        self.name = name


def user_from_db(db: Database, id: str):
    result = db['users'].find_one({'uuid':id})
    return User(result['uuid'], result['name'])
