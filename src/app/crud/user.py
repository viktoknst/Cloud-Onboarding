import os
import


def create(user_name):
    if re.match(r'^[a-zA-Z0-9_-]{4,16}$', u.user_name) == None:
        raise HTTPException(409, "Username is invalid")

    if os.path.exists(USER_DB['user_dir']+"/"+u.user_name):
        raise HTTPException(409, "Username is in use!")

    os.mkdir(USER_DB['user_dir']+"/"+u.user_name)
    return {'msg': 'User created'}

def read():

def update

def delete():
