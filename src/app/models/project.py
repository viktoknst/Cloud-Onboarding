class Project:
    id: str
    entry_file: str
    source_dir: str


    def __init__(self, id: str, entry_file: str, source_dir: str):
        self.id = id
        self.entry_file = entry_file
        self.source_dir = source_dir
