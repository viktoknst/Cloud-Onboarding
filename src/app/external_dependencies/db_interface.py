"""
File which gives db connections.
"""

from pymongo import MongoClient

CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.10"

class DBProxy:
    """
    Singleton which holds the db client.
    (unnescessary as mongoclient is threadsafe but thats not stopping me)
    """
    __instance = None


    def __init__(self):
        """
        s.e.
        """
        self.client = MongoClient(CONNECTION_STRING)


    @classmethod
    def get_instance(cls):
        """
        Returns db client instance
        """
        if cls.__instance is None:
            cls.__instance = DBProxy()
        return cls.__instance


    def get_db(self):
        """
        get DB connection

        Returns:
            Database: PyMongo database
        """
        return self.client['cob_db']
