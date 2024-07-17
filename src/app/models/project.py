class Project:
    id: str
    name: str
    entry_file: str
    source_dir: str
    user_id: str

    def __init__(self, id: str, name: str, entry_file: str, source_dir: str, user_id: str):
        self.id = id
        self.name = name
        self.entry_file = entry_file
        self.source_dir = source_dir
        self.user_id = user_id
