from pymongo.database import Database


def login(db: Database, username: str) -> str | None:
    result = db['users'].find_one(username)
    if result == None:
        return None
    return result['id']
