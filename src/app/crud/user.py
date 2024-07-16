from pymongo.database import Database
from app.models.user import User
from app.special.config import USERS_DIRECTORY

import uuid
import os
import re
import shutil


def create(db: Database, user_name):
    if re.match(r'^[a-zA-Z0-9_-]{4,16}$', user_name) == None:
        return "Username is invalid"

    if db['users'].find_one({'name': user_name}) != None:
        return "Username is in use!"

    if os.path.exists(USERS_DIRECTORY+'/'+user_name):
        return "Fatal error!"
        # shutil.rmtree(USERS_DIRECTORY+'/'+user_name)

    db['users'].insert_one(
        {
            'id': uuid.uuid4(),
            'name': user_name,
            'dir': USERS_DIRECTORY+'/'+user_name
        }
    )
    os.mkdir(USERS_DIRECTORY+'/'+user_name)


def read(db: Database, id: str) -> User | str:
    result = db['users'].find_one({'id':id})

    if result == None:
        return "User not found error!"

    return User(
        result['id'],
        result['name'],
        result['dir']
    )


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
