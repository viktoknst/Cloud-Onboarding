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
    '''
    Project model
    '''
    db: Database

    @classmethod
    def set_db(cls, db: Database):
        cls.db = db


    def __init__(self,
                id: str,
                name: str,
                entry_file: str,
                source_dir: str,
                user_id: str
        ):
        '''
        Private
        '''
        self.id = id
        self.name = name
        self.entry_file = entry_file
        self.source_dir = source_dir
        self.user_id = user_id


    @classmethod
    def create(cls, user: User, name: str):
        if re.match(r'^[a-zA-Z0-9_-]{4,16}$', name) is None:
            raise Exception("Project name is invalid")

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
        '''
        Saves the state of the object to the db.
        '''
        self.db['projects'].update_one(
            filter={
                'id': self.id
            },
            update={'$set':{
                #'id':, explicitly ommitted
                'name': self.name,
                'entry_file': self.entry_file,
                'source_dir': self.source_dir,
                #'user_id': user_id explicitly ommitted
            }}
        )


    def delete(self) -> None:
        #if not os.path.exists(self.source_dir):
        #    raise Exception("Faulty deletion; Aborting")
        shutil.rmtree(self.source_dir)
        self.db['projects'].delete_one({'id':self.id})


    def add_dir(self, dir_path: str):
        if os.path.isdir(self.source_dir+'/'+dir_path):
            return
        os.mkdir(self.source_dir+'/'+dir_path)


    def add_file(self, file_path: str, file: BinaryIO, is_entry: bool):
        """Adds a file to the project

        Args:
            file (BinaryIO): File data
            filename (str): File name
            is_entry (bool): Is the file an entry point
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


    def to_jsons(self):
        '''
        To JSON string.
        '''
        return json.dumps(
            self.to_dict()
        )


    def to_dict(self):
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
