from docker.models.containers import Container
from multiprocessing import Process
import uuid

from pymongo.database import Database
import app.crud.result_crud as results
from app.models.result import Result

class ProjectInstance:
    id: str
    container: Container
    db: Database
    thread: Process

    def __init__(self, container: Container, db: Database):
        self.id = str(uuid.uuid4())
        #self.id = Container.id_attribute
        self.container = container
        self.db = db
        thread = Process(target=self.run, args=[])
        thread.daemon = False
        self.thread = thread

    def run(self):
        results.create(self.db, self.id)
        self.container.start()
        self.container.wait() # takes a long while...
        result = self.container.logs().decode()
        results.update(self.db, Result(self.id, result))

    def start(self):
        self.thread.start()

# Used by project
