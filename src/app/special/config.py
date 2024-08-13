'''
Holds congiguration option
'''
from os.path import abspath, join, dirname, isdir

from os.path import abspath, join

ENDPOINTS = {
    'discovery'     : '/',
    'create_user'   : '/new',
    'login'         : '/login',
    'user'          : '/user',
    'project'       : '/project',
    'create_project' : '/project/new',
    'result'        : '/result',
}

# God awful
USERS_DIRECTORY = abspath(join(dirname(__file__), "..", "..", "..", "users"))
assert isdir(USERS_DIRECTORY), f"User directory (/users) does not exist! (is {USERS_DIRECTORY})"
