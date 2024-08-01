from multiprocessing import Process
import uuid
from docker.models.containers import Container

from pymongo.database import Database
from app.crud.result_crud import Result

class ProjectInstance:
    id: str
    container: Container
    thread: Process


    def __init__(self, container: Container):
        self.id = str(uuid.uuid4())
        #self.id = Container.id_attribute
        self.container = container
        thread = Process(target=self.run, args=[])
        thread.daemon = False
        self.thread = thread


    def run(self):
        result = Result.create(None)

        self.container.start()
        self.container.wait() # takes a long while...
        result_str = self.container.logs().decode()

        result.result = result_str
        result.update()


    def start(self):
        self.thread.start()

# Used by project
