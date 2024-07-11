from docker.models.containers import Container
from multiprocessing import Process
import uuid

import db_interface

class ProjectInstance:
    id: str
    container: Container
    thread: Process
    def __init__(self, container):
        self.id = str(uuid.uuid4())
        self.container = container
        thread = Process(target=self.run, args=[])
        thread.daemon = False
        self.thread = thread

    def run(self):
        db_interface.results.insert_one({'uuid': self.id, 'status': 'running'})
        self.container.start()
        self.container.wait()
        result = self.container.logs().decode()
        db_interface.results.update_one({'uuid': self.id},{'$set':{'status': 'done', 'result':result}})

    def start(self):
        self.thread.start()
