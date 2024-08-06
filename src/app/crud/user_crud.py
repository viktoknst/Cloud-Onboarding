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
    """
    Object representation of a user's project.
    Handles saving/reading from a db.
    Expects a mong-like db interface.
    """
    db: Database

    @classmethod
    def set_db(cls, db: Database):
        """Sets the database to be used by the class and all its instances.

        Args:
            db (Database): A mongo-like db
        """
        cls.db = db


    def __init__(self, id: str, name: str, dir: str, password_hash: str, salt: str):
        """
        Constructor sets fields without checking them. Private.
        
        Args:
            id (str): User id, string uuid4.
            name (str): User name.
            dir (str): Full path to the user directory, for saving projects.
            password_hash (str): Securely generated hash of the user password.
            salt (str): Used for hash generation.
        """
        self.id = id
        self.name = name
        self.dir = dir
        self.password_hash = password_hash
        self.salt = salt


    @classmethod
    def create(cls, name: str, password: str):
        """
        Creates a user in db and file system.
        Returns the resulting user object.

        Args:
            name (str): User
            password (str): User password

        Raises:
            ValueError: User name is invalid\n
            ValueError: Password is invalid\n
            ValueError: User name is in use\n
            Exception: User directory is in use/already exist

        Returns:
            User: The resulting user object
        """
        cls.__validate_name(name)
        cls.__validate_password(password)

        if cls.db['users'].find_one({'name': name}) is not None:
            raise ValueError("Username is in use!")

        id = str(uuid.uuid4())
        dir = USERS_DIRECTORY+'/'+name

        if os.path.exists(dir):
            raise Exception("Fatal error!")
            # shutil.rmtree(USERS_DIRECTORY+'/'+user_name)

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
        """
        Reads a user from db.
        Requires either user id or user name.
        If neither are provided, throws an exception.
        If the user doesnt exist, throws an exception.

        Args:
            id (str | None, optional): User id. Defaults to None.
            name (str | None, optional): User name. Defaults to None.

        Raises:
            ValueError: No identifying arguments provided
            ValueError: The user was not found

        Returns:
            User: The user from the db
        """
        if id is not None:
            user_dict = cls.db['users'].find_one({'id':id})
        if name is not None:
            user_dict = cls.db['users'].find_one({'name':name})
        else:
            raise ValueError('No arguments provided')
        if user_dict is None:
            raise ValueError('User not found')
        return User(
            user_dict['id'],
            user_dict['name'],
            user_dict['dir'],
            user_dict['password_hash'],
            user_dict['salt'],
        )


    def update(self) -> None:
        """
        Saves the current state of the object (fields) to the db.
        Some fields that should not be altered are not saved.
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
        """
        Deletes project from database and the file system.
        Does not alter the object itself.
        If deleting from FS failed, throws exception but still deletes from db.
        Raises:
            Exception: On user dir removal failure
        """
        self.db['users'].delete_one({'id':self.id})
        if not os.path.exists(self.dir):
            raise Exception("Faulty deletion")
        shutil.rmtree(self.dir)


    def to_jsons(self) -> str:
        """
        To json string.

        Returns:
            str: Json string of the object
        """
        return json.dumps(
            self.to_dict()
        )


    def to_dict(self) -> any:
        """To dictionary of object fields.

        Returns:
            dict: Dictionary with the object fields, with their names as keys.
        """
        return{
                'id': self.id,
                'name': self.name,
                'dir': self.dir,
                'password_hash': self.password_hash,
                'salt': self.salt,
            }


    def change_password(self, new_password: str) -> None:
        """
        Changes the user password.
        Validates it, generates new salt+hash.
        Must `.update()` for change to take effect.

        Args:
            new_password (str): The new password.

        Raises:
            ValueError: Invalid password
        """
        salt = auth_utils.gen_salt()
        password_hash = auth_utils.hash_password(new_password, salt)
        self.__validate_password(new_password)
        self.salt = salt
        self.password_hash = password_hash


    @classmethod
    def __validate_name(cls, name: str):
        """
        Ensures string is a valid user name.

        Raises:
            ValueError: Username invalid
        """
        if re.fullmatch(r'^[a-zA-Z0-9 _-]{4,16}$', name) is None:
            raise ValueError("Username is invalid!")


    @classmethod
    def __validate_password(cls, password: str):
        """
        Ensures string is a valid password.

        Raises:
            ValueError: Password invalid
        """
        if re.fullmatch(r'^[a-zA-Z0-9 _-]{4,16}$', password) is None:
            raise ValueError("Password is invalid!")
