from pymongo.database import Database
from app.models.user import User
from app.special.config import USERS_DIRECTORY

import uuid
import os
import re
import shutil
from app.services import auth_utils

# import asyncio.locks TODO: we have 0 protection against concurent user creation:
# A creates user John
# B creates user John
# A sees John doesnt exist
# B sees Jogn doesnt exist
# A inserts one John into DB
# B inserts another Jogn into DB
# XO

def create(db: Database, user_name, password):
    salt = auth_utils.gen_salt()
    password_hash = auth_utils.hash_password(password, user_name, salt)

    if re.match(r'^[a-zA-Z0-9 _-]{4,16}$', user_name) == None:
        return "Username is invalid"

    if db['users'].find_one({'name': user_name}) != None:
        return "Username is in use!"

    if os.path.exists(USERS_DIRECTORY+'/'+user_name):
        return "Fatal error!"
        # shutil.rmtree(USERS_DIRECTORY+'/'+user_name)

    db['users'].insert_one(
        {
            'id': str(uuid.uuid4()),
            'name': user_name,
            'dir': USERS_DIRECTORY+'/'+user_name,
            'password_hash': password_hash,
            'salt': salt,
        }
    )
    os.mkdir(USERS_DIRECTORY+'/'+user_name)


def read(db: Database, id: str | None = None, name: str | None = None) -> User | str:
    result = None
    if id != None:
        result = db['users'].find_one({'id':id})
    if name != None:
        result = db['users'].find_one({'name':name})

    if result == None:
        return "User not found error!"

    return User(
        result['id'],
        result['name'],
        result['password'],
        result['dir']
    )

#def read(db: Database, id: str) -> User | str:
#    result = db['users'].find_one({'id':id})
#
#    if result == None:
#        return "User not found error!"
#
#    return User(
#        result['id'],
#        result['name'],
#        result['password'],
#        result['dir']
#    )


def update(db: Database, user: User) -> User:
    result = db['users'].find_one({'id':user.id})

    db['users'].update_one(
        {
            'name': user.name
        }
    )


def delete(db: Database, id: str):
    result = db['users'].find_one({'id':id})

    if result == None:
        return "User not found"

    if not os.path.exists(result['dir']):
        return "Faulty deletion; Aborting"

    db['users'].delete_one({'id':id})
    shutil.rmtree(result['dir'])
