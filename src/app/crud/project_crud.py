"""
Module that handles CRUD operations for projects in the DB
"""

import re
import os
import uuid

from pymongo.database import Database

from app.models.project import Project


def create(db: Database, user_id: str, project_name):
    user = db['users'].find_one({'id':user_id})
    if user is None:
        return "User cant create project; User does not exist"

    if re.match(r'^[a-zA-Z0-9_-]{4,16}$', project_name) is None:
        return "Project name is invalid"

    if db['projects'].find_one({'user_id': user_id, 'name': project_name}) is not None:
        return "User has another project of the same name"

    if os.path.exists(user['dir']+'/'+project_name):
        return "Fatal error!"
        # shutil.rmtree(USERS_DIRECTORY+'/'+user_name)

    db['projects'].insert_one(
        {
            'id': str(uuid.uuid4()),
            'name': project_name,
            'entry_file': None,
            'source_dir': None,
            'user_id': user_id
        }
    )
    # replace with mktemp -d, creates a randomly named, non-existant directory
    os.mkdir(user['dir']+'/'+project_name)

def read(db: Database, project_id: str) -> Project:
    project_dict = db['projects'].find_one({'id': project_id})
    return Project(
        project_dict['id'],
        project_dict['name'],
        project_dict['entry_file'],
        project_dict['source_dir'],
        project_dict['user_id']
    )

def update(db: Database, p: Project):
    db['projects'].update_one(
        {
            #'id':,
            'name': p.project_name,
            'entry_file': p.entry_file,
            'source_dir': p.entry_file,
            #'user_id': user_id
        }
    )


def delete(db: Database, id: str):
    return db['projects'].delete_one(
        {
            'id': id,
        }
    )
