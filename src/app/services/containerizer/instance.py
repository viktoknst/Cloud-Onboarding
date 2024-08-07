from multiprocessing import Process
from docker.models.containers import Container
from docker.models.images import Image

from app.crud.result_crud import Result

class ProjectInstance:
    def __init__(self, container: Container, image: Image):
        self.result = Result.create(None)
        self.container = container
        self.image = image

        thread = Process(target=self.run, args=[])
        thread.daemon = False
        self.thread = thread


    def run(self):
        self.container.start()
        self.container.wait() # takes a long while...
        result_str = self.container.logs().decode()
        self.container.remove()
        self.image.remove(force=True)

        self.result.result = result_str
        self.result.status = 'done'
        self.result.update()


    def start(self):
        self.thread.start()


# Used by project
