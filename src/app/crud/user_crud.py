"""
Module that handles CRUD operations for users in the DB
"""

import uuid
import os
import re
import shutil
import json

from pymongo.database import Database

from app.special.config import USERS_DIRECTORY
from app.services import auth_utils

class User:
    '''
    User model
    '''
    db: Database

    @classmethod
    def set_db(cls, db: Database):
        cls.db = db


    def __init__(self, id: str, name: str, dir: str, password_hash: str, salt: str):
        self.id = id
        self.name = name
        self.dir = dir
        self.password_hash = password_hash
        self.salt = salt


    @classmethod
    def create(cls, name: str, password: str):
        """Creates user into the given DB. Throws exceptions.

        Args:
            mongo_db (Database): _description_
            user_name (str): _description_
            password (str): _description_

        Returns:
            None
        """

        cls.__validate_name(name)
        cls.__validate_password(password)

        if cls.db['users'].find_one({'name': name}) is not None:
            raise ValueError("Username is in use!")

        dir = USERS_DIRECTORY+'/'+name

        if os.path.exists(dir):
            raise Exception("Fatal error!")
            # shutil.rmtree(USERS_DIRECTORY+'/'+user_name)

        id = str(uuid.uuid4())

        salt = auth_utils.gen_salt()
        password_hash = auth_utils.hash_password(password, salt)

        user = User(id, name, dir, password_hash, salt)

        os.mkdir(dir)

        cls.db['users'].insert_one(
            json.loads(user.to_jsons())
        )

        return user


    @classmethod
    def read(cls, id: str | None = None, name: str | None = None):
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
        if id is not None:
            user_dict = cls.db['users'].find_one({'id':id})
        if name is not None:
            user_dict = cls.db['users'].find_one({'name':name})
        if user_dict is None:
            raise Exception("User not found!")

        return User(
            user_dict['id'],
            user_dict['name'],
            user_dict['dir'],
            user_dict['password_hash'],
            user_dict['salt'],
        )


    def update(self) -> None:
        """Updates user in the given DB.
        Only fileds not equal to '' will be updated.
        'user' MUST have id.

        Args:
            mongo_db (Database): _description_
            user (User): _description_

        Returns:
            User: The User that resulted from the change.
        """

        self.__validate_name(self.name)

        self.db['users'].update_one(
            {
                'id':self.id
            },
            {'$set':{
                # id is explicitly ignored; it makes 0 sense to change it
                'name': self.name,
                'dir': self.dir,
                'password_hash': self.password_hash,
                'salt': self.salt,
            }}
        )


    def delete(self) -> None:
        """Deletes user from DB.

        Args:
            user_db (Database): _description_
            user_id (str): _description_

        Returns:
            _type_: _description_
        """

        if not os.path.exists(self.dir):
            raise Exception("Faulty deletion; Aborting")
        shutil.rmtree(self.dir)
        self.db['users'].delete_one({'id':self.id})


    def to_jsons(self) -> str:
        return json.dumps(
            self.to_dict()
        )


    def to_dict(self) -> any:
        return{
                'id': self.id,
                'name': self.name,
                'dir': self.dir,
                'password_hash': self.password_hash,
                'salt': self.salt,
            }


    def change_password(self, new_password: str) -> None:
        salt = auth_utils.gen_salt()
        password_hash = auth_utils.hash_password(new_password, salt)
        self.__validate_password(new_password)
        self.salt = salt
        self.password_hash = password_hash


    @classmethod
    def __validate_name(cls, name: str):
        '''
        Throws VallueError
        '''
        if re.fullmatch(r'^[a-zA-Z0-9 _-]{4,16}$', name) is None:
            raise ValueError("Username is invalid!")


    @classmethod
    def __validate_password(cls, password: str):
        '''
        Throws VallueError
        '''
        if re.fullmatch(r'^[a-zA-Z0-9 _-]{4,16}$', password) is None:
            raise ValueError("Password is invalid!")

# import asyncio.locks TODO: we have 0 protection against concurent user creation:
# A creates user John
# B creates user John
# A sees John doesnt exist
# B sees Jogn doesnt exist
# A inserts one John into DB
# B inserts another Jogn into DB
# XO
