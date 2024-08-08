from multiprocessing import Process
import uuid
from docker.models.containers import Container
from docker.models.images import Image

from pymongo.database import Database
from app.crud.result_crud import Result

class ProjectInstance:
    def __init__(self, container: Container):
        self.result = Result.create(None)
        self.container = container

        thread = Process(target=self.run, args=[])
        thread.daemon = False
        self.thread = thread


    def run(self):
        self.container.start()
        self.container.wait() # takes a long while...
        result_str = self.container.logs().decode()
        self.container.remove()

        self.result.result = result_str
        self.result.status = 'done'
        self.result.update()


    def start(self):
        self.thread.start()


# Used by project
