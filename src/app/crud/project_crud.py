"""
Module that handles CRUD operations for projects in the DB
"""

import re
import os
import uuid
import json

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

#    def set_name(self, new_name: str):
#        if re.match(r'^[a-zA-Z0-9_-]{4,16}$', new_name) is None:
#            raise Exception("Project name is invalid")

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
            raise Exception('No arguments provided')
        if project_dict is None:
            raise Exception('User not found')
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
                'source_dir': self.entry_file,
                #'user_id': user_id explicitly ommitted
            }}
        )


    def delete(self) -> None:
        self.db['projects'].delete_one({'id': self.id})
        os.rmdir(self.source_dir)


    # TODO
    def add_file(self, file):
        pass


    def to_jsons(self):
        '''
        To JSON string.
        '''
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'entry_file': self.entry_file,
            'source_dir': self.source_dir,
            'user_id': self.user_id,
        })

#class User:
#       def __init__(self, id, dir):
#        self.id = id
#        self.dir = dir
#import mongomock
#if __name__ == '__main__':
#    a_user = User('abc123','/home/sasho_b/Coding/cob2/users')
#    Project.set_db(mongomock.MongoClient().get_database('mydb'))
#
#    os.rmdir('/home/sasho_b/Coding/cob2/users/myproject')
#    myproject = Project.create(a_user, 'myproject')
#    myproject.name = 'new_name'
#    the_id = myproject.id
#    myproject.update()
#    project_by_id = Project.read(a_user, id=the_id)
#    assert myproject.name == project_by_id.name
#    project_by_name = Project.read(a_user, name='new_name')
#    assert myproject.id == project_by_name.id
#
