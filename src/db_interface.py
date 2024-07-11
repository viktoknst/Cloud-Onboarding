from pymongo import MongoClient

import uuid

CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.10"

db_client = MongoClient(CONNECTION_STRING)

database = db_client['cob_db']

users = database['users']
projects = database['projects']
instances = database['instances']
results = database['results']
