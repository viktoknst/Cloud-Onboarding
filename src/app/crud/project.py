import docker
from docker.models.images import Image

from pathlib import Path
import uuid

from src.containerizer.instance import ProjectInstance
from src import db_interface as db

ROOT = Path("/home/sasho_b/Coding/cob/docker")
DOCKER_TEMPLATE = Path(ROOT, "dockerfile_template")

CLIENT = docker.from_env()

def create_project_in_db():
    id = str(uuid.uuid4())
    db.projects.insert_one()


def get_project_from_db(id: str):
    result = db.projects.find_one()


class Project:
    entry_file: str
    source_dir: str
    #def __init__(self, entry_file: str, source_dir: str):
    #    self.id = str(uuid.uuid4())
    #    self.entry_file = entry_file
    #    self.source_dir = source_dir


    def __init__(self, entry_file: str, source_dir: str):
        self.entry_file = entry_file
        self.source_dir = source_dir
        # get out metadata for image and project from mongo and docker.images


    def create():
        pass
    def read():
        pass
    def update():
        pass
    def delete():
        pass


    def create_detached_instance(self):
        self.fillout_template()

        image = CLIENT.images.build(path=str(self.source_dir), rm=True)[0] # rm=True OR IT BREAKS!
        container = CLIENT.containers.create(image.id)

        instance = ProjectInstance(container)
        instance.start()

        image.remove(force=True)

        return instance.id


    def fillout_template(self) -> None:
        template = ''
        entry_file = Path(self.entry_file)

        with open(DOCKER_TEMPLATE, 'r') as file:
            template = file.read()
            template = template.replace('{entry_file}', entry_file.name)

        with open(Path(self.source_dir,"Dockerfile"), "w+") as save_to:
            save_to.write(template)


if __name__ == '__main__':
    p = Project('/home/sasho_b/Coding/debug_cob/main.py', '/home/sasho_b/Coding/debug_cob')
    id = p.create_detached_instance()
    print(id)
