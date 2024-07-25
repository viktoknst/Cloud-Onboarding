'''
File which connects to the DB
'''

from pymongo import MongoClient

CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.10"

class DBProxy:
    '''
    singleton which holds the db; unnescessary as mongoclient is threadsafe but thats not stopping me
    '''
    __instance = None

    def __init__(self):
        self.client = MongoClient(CONNECTION_STRING)


    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = DBProxy()
        return cls.__instance


    def get_db(self):
        return self.client['cob_db']

# NOTE: use with FastAPI `Depends()` parameter, as db: DBProxy = Depends(DBProxy.get_instance()) ok?
