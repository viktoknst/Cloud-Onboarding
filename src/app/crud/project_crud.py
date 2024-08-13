"""
Module that handles CRUD operations for projects in the DB
"""

import re
import os
import uuid
import json
from typing import BinaryIO
import shutil

from pymongo.database import Database

from app.crud.user_crud import User


class Project:
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


    def __init__(
            self,
            id: str,
            name: str,
            entry_file: str,
            source_dir: str,
            user_id: str
        ):
        """
        Constructor sets fields without checking them. Private.
        
        Args:
            id (str): Project id, uuid4.
            name (str): Project name.
            entry_file (str): The file to be executed first when project is ran.
            source_dir (str): Root directory for saving project uploads.
            user_id (str): Id of the owner.
        """
        self.id = id
        self.name = name
        self.entry_file = entry_file
        self.source_dir = source_dir
        self.user_id = user_id


    @classmethod
    def create(cls, user: User, name: str):
        """
        Creates a project in db and file system.
        Returns the resulting project object.

        Args:
            user (User): The owner to create said project
            name (str): The project name

        Raises:
            Exception: Project name is invalid\n
            Exception: User has project of the same name\n
            Exception: Project dir already exists

        Returns:
            Project: The resulting project object
        """
        if re.match(r'^[a-zA-Z0-9_-]{4,16}$', name) is None:
            raise Exception("Project name is invalid") # TODO to value errs

        if cls.db['projects'].find_one(
            {
                'user_id': user.id,
                'name': name
            }
        ) is not None:
            raise Exception("User has another project of the same name")

        source_dir = user.dir+'/'+name

        if os.path.exists(source_dir):
            # shutil.rmtree(USERS_DIRECTORY+'/'+user_name)
            raise Exception("Fatal error!")

        id = str(uuid.uuid4())

        cls.db['projects'].insert_one(
            {
                'id': id,
                'name': name,
                'entry_file': None,
                'source_dir': source_dir,
                'user_id': user.id
            }
        )
        # replace with mktemp -d, creates a randomly named, non-existant directory
        os.mkdir(source_dir)
        return Project(id, name, None, source_dir, user.id)


    @classmethod
    def read(cls, user: User, id: str | None = None, name: str | None = None):
        """
        Reads a project from db.
        Requires the owner and either project id or proejct name.
        If neither are provided, throws an exception.
        If the project doesnt exist, throws an exception.

        Args:
            user (User): Owner of the project
            id (str | None, optional): Project id. Defaults to None.
            name (str | None, optional): Project name. Defaults to None.

        Raises:
            ValueError: No identifying arguments provided
            ValueError: The project was not found

        Returns:
            Project: The project from the db
        """
        if id is not None:
            project_dict = cls.db['projects'].find_one({'id': id})
        elif name is not None:
            project_dict = cls.db['projects'].find_one({'name': name, 'user_id': user.id})
        else:
            raise ValueError('No arguments provided')
        if project_dict is None:
            raise ValueError('Project not found')
        return Project(
            project_dict['id'],
            project_dict['name'],
            project_dict['entry_file'],
            project_dict['source_dir'],
            project_dict['user_id']
        )


    def update(self) -> None:
        """
        Saves the current state of the object (fields) to the db.
        Some fields that should not be altered are not saved.
        """
        self.db['projects'].update_one(
            filter={
                'id': self.id
            },
            update={'$set':{
                #'id': id explicitly ommitted
                'name': self.name,
                'entry_file': self.entry_file,
                'source_dir': self.source_dir,
                #'user_id': user_id explicitly ommitted
            }}
        )


    def delete(self) -> None:
        """
        Deletes project from database and the file system.
        Does not alter the object itself.
        """
        #if not os.path.exists(self.source_dir):
        #    raise Exception("Faulty deletion; Aborting")
        self.db['projects'].delete_one({'id':self.id})
        shutil.rmtree(self.source_dir)


    def add_dir(self, dir_path: str):
        if os.path.isdir(self.source_dir+'/'+dir_path):
            return
        os.mkdir(self.source_dir+'/'+dir_path)


    def add_file(self, file_path: str, file: BinaryIO, is_entry: bool) -> None:
        """
        Adds a file to the file directory.
        If another file of the same name exists - overwrites it.
        If `is_entry` is set to true, the file is set as the project entry point.
        Updates the project in db accordingly.
        Args:
            file (BinaryIO): The file data in binary
            file_path (str): The name to write to
            is_entry (bool): Is project entry point
        """
        file_location = f"{self.source_dir}/{file_path}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.read())
        if is_entry is True:
            self.entry_file = file_path
            self.update()


    def remove_file(self, file_path: str):
        """Removes file OR directory tree

        Args:
            file_path (str): the object to delete

        Raises:
            ValueError: Path does not exist
        """
        if not os.path.exists(self.source_dir+'/'+file_path):
            raise ValueError(f"{file_path} does not exist!")
        if os.path.isfile(self.source_dir+'/'+file_path):
            os.remove(self.source_dir+'/'+file_path)
        else:
            shutil.rmtree(self.source_dir+'/'+file_path)


    def to_jsons(self) -> str:
        """To json string.
        
        Returns:
            str: Json formated string of the object
        """
        return json.dumps(
            self.to_dict()
        )


    def to_dict(self) -> dict:
        """To dictionary of object fields.

        Returns:
            dict: Dictionary with the object fields, with their names as keys.
        """
        return {
            'id': self.id,
            'name': self.name,
            'entry_file': self.entry_file,
            'source_dir': self.source_dir,
            'user_id': self.user_id,
        }


    def read_file_structure(self):
        """
        Dir to json-esque dict
        """
        tree = {}
        for root, dirs, files in os.walk(self.source_dir):
            subdir = tree
            for part in root.replace(self.source_dir, '').strip(os.sep).split(os.sep):
                if part:
                    subdir = subdir.setdefault(part, {})
            for d in dirs:
                subdir[d] = {}
            for f in files:
                subdir[f] = 'file'
        return tree


    def set_dependencies(self, dependency_list: list):
        pass
