'''
Holds congiguration option
'''

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

USERS_DIRECTORY = abspath(join(abspath(__file__), '../../../../users'))
