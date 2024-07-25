"""
Module that handles CRUD operations for users in the DB
"""

import uuid
import os
import re
import shutil

from pymongo.database import Database

from app.models.user import User
from app.special.config import USERS_DIRECTORY
from app.services import auth_utils

# import asyncio.locks TODO: we have 0 protection against concurent user creation:
# A creates user John
# B creates user John
# A sees John doesnt exist
# B sees Jogn doesnt exist
# A inserts one John into DB
# B inserts another Jogn into DB
# XO

def create(mongo_db: Database, user_name: str, password: str) -> None:
    """Creates user into the given DB. Throws exceptions.

    Args:
        mongo_db (Database): _description_
        user_name (str): _description_
        password (str): _description_

    Returns:
        None
    """
    salt = auth_utils.gen_salt()
    password_hash = auth_utils.hash_password(password, user_name, salt)

    if re.match(r'^[a-zA-Z0-9 _-]{4,16}$', user_name) is None:
        raise ValueError("Username is invalid")

    if db['users'].find_one({'name': user_name}) is not None:
        raise Exception("Username is in use!")

    if os.path.exists(USERS_DIRECTORY+'/'+user_name):
        raise Exception("Fatal error!")
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


def read(mongo_db: Database, user_id: str | None = None, user_name: str | None = None) -> User:
    """Reads user from the given DB. Throws exceptions.
    Can search either by name or id. If neither are provided, user cant be found.

    Args:
        mongo_db (Database): _description_
        user_id (str | None, optional): _description_. Defaults to None.
        user_name (str | None, optional): _description_. Defaults to None.

    Returns:
        User: _description_
    """
    user_dict = None
    if user_id is not None:
        user_dict = mongo_db['users'].find_one({'id':user_id})
    if user_name is not None:
        user_dict = mongo_db['users'].find_one({'name':user_name})

    if user_dict is None:
        raise Exception("User not found!")

    return User(
        user_dict['id'],
        user_dict['name'],
        user_dict['dir'],
        user_dict['password_hash'],
        user_dict['salt'],
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


def update(mongo_db: Database, user: User) -> User:
    """Updates user in the given DB.
    Only fileds not equal to '' will be updated.
    'user' MUST have id.

    Args:
        mongo_db (Database): _description_
        user (User): _description_

    Returns:
        User: The User that resulted from the change.
    """
    old_user = read(mongo_db=mongo_db, user_id=user.id)
    if user.name == '':
        user.name = old_user.name
    if user.dir == '':
        user.dir = old_user.dir
    if user.password_hash == '':
        user.password_hash = old_user.password_hash
    if user.salt == '':
        user.salt = old_user.salt
    mongo_db['users'].update_one(
        {
            # id is explicitly ignored; it makes 0 sense to change it
            'name': user.name,
            'dir': user.dir,
            'password_hash': user.password_hash,
            'salt': user.salt,
        }
    )


def delete(user_db: Database, user_id: str):
    """Deletes user from DB.

    Args:
        user_db (Database): _description_
        user_id (str): _description_

    Returns:
        _type_: _description_
    """
    user_dict = user_db['users'].find_one({'id': user_id})
    if user_dict is None:
        raise Exception("User not found")

    if not os.path.exists(user_dict['dir']):
        raise Exception("Faulty deletion; Aborting")

    user_db['users'].delete_one({'id':user_id})
    shutil.rmtree(user_dict['dir'])
