"""
File for generating docker containers
"""
from multiprocessing import Process

import docker
from docker.models.containers import Container

from app.crud.result_crud import Result
from app.crud.project_crud import Project, ProjectType

CLIENT = docker.from_env()


def create_detached_instance(p: Project):
    """
    Creates a ProjectInstance with an apropriate container based on Project.project_type
    
    Returns: ProjectInstance
    """
    if p.project_type == ProjectType.python:
        image = CLIENT.images.get("python")
        container = CLIENT.containers.create(
            image.id,
            command=f"timeout --verbose 10 python /src/{p.entry_file}",
            volumes={p.source_dir: {'bind': '/src', 'mode': 'ro'}}
        )
    if p.project_type == ProjectType.js:
        image = CLIENT.images.get("node:16")
        container = CLIENT.containers.create(
            image.id,
            command=f"timeout --verbose 10 node /src/{p.entry_file}",
            volumes={p.source_dir: {'bind': '/src', 'mode': 'ro'}}
        )
    if p.project_type == ProjectType.bin:
        image = CLIENT.images.get("alpine")
        container = CLIENT.containers.create(
            image.id,
            command=f"timeout --verbose 10 ./src/{p.entry_file}",
            volumes={p.source_dir: {'bind': '/src', 'mode': 'ro'}}
        )
    instance = ProjectInstance(container)
    return instance


class ProjectInstance:
    """
    Takes a container with a project,
    starts it, saves the result and cleans up.
    Note: While it is implemented as a thread,
    FastAPI breaks it. Use BackgroundTask(.run()) instead of .start().
    """
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
