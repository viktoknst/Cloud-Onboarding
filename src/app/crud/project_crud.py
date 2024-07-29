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
        raise Exception("User cant create project; User does not exist")

    if re.match(r'^[a-zA-Z0-9_-]{4,16}$', project_name) is None:
        raise Exception("Project name is invalid")

    if db['projects'].find_one({'user_id': user_id, 'name': project_name}) is not None:
        raise Exception("User has another project of the same name")

    if os.path.exists(user['dir']+'/'+project_name):
        raise Exception("Fatal error!")
        # shutil.rmtree(USERS_DIRECTORY+'/'+user_name)
    project_id = str(uuid.uuid4())
    db['projects'].insert_one(
        {
            'id': project_id,
            'name': project_name,
            'entry_file': None,
            'source_dir': user['dir']+'/'+project_name,
            'user_id': user_id
        }
    )
    # replace with mktemp -d, creates a randomly named, non-existant directory
    os.mkdir(user['dir']+'/'+project_name)
    return project_id


def read(db: Database, project_id: str | None = None, project_name: str | None = None) -> Project:
    project_dict = None
    if project_id is not None:
        project_dict = db['projects'].find_one({'id': project_id})
    elif project_name is not None:
        project_dict = db['projects'].find_one({'name': project_name})
    else:
        raise Exception('No arguments provided')
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


def delete(db: Database, project_id: str | None = None, project_name: str | None = None):
    project_dict = None
    if project_id is not None:
        project_dict = db['projects'].find_one_and_delete({'id': project_id})
    elif project_name is not None:
        project_dict = db['projects'].find_one_and_delete({'name': project_name})
    else:
        raise Exception('No arguments provided')
    os.rmdir(project_dict['source_dir'])
