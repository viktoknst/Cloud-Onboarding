from pymongo import MongoClient

CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.10"

#class DBProxy:
#    __instance = None
#
#    def __init__(self):
#        __instance = MongoClient(CONNECTION_STRING)
#
#    def get_instance(cls):
#        if cls.__instance == None:
#            cls.__instance = DBProxy()
#        return cls.__instance

db_client = MongoClient(CONNECTION_STRING)
database = db_client['cob_db']

users = database['users']
projects = database['projects']
instances = database['instances']
results = database['results']
