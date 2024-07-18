class User:
    id: str
    name: str
    dir: str
    password_hash: str
    salt: str

    def __init__(self, id, name, dir, password_hash, salt):
        self.id = id
        self.name = name
        self.dir = dir
        self.password_hash = password_hash
        self.salt = salt
