import docker
from docker.models.images import Image

from pathlib import Path

from instance import ProjectInstance

import db_interface as db

ROOT = Path("/home/sasho_b/Coding/cob/docker")
DOCKER_TEMPLATE = Path(ROOT, "dockerfile_template")

CLIENT = docker.from_env()

def fillout_template(entry_file: Path, source_dir: Path) -> None:
    template = ''
    with open(DOCKER_TEMPLATE, 'r') as file:
        template = file.read()
        template = template.replace('{entry_file}', entry_file.name)
    with open(Path(source_dir,"Dockerfile"), "w+") as save_to:
        save_to.write(template)

class Project:
    id: str
    image: Image
    entry_file: str
    source_dir: str
    def __init__(self, id: str):
        result = db.projects.find_one({'uuid':id})
        self.id = id
        self.entry_file = result['entry_file']
        self.source_dir = result['source_dir']
        CLIENT.images.get()
        # get out metadata for image and project from mongo and docker.images

    def create_instance(self):
        fillout_template(self.entry_file, self.source_dir)
        image = CLIENT.images.build(path=str(self.source_dir), rm=True)[0] # rm=True OR IT BREAKS!
        container = CLIENT.containers.create(image.id)
        instance = ProjectInstance(container)
        instance.start()
        image.remove(force=True)


# TODO FIGURE OUT WHAT TO DO WITH THE INSTANCES; NOTE - WHERE DO THEY EXIST? IN THEIR THREAD? IDK
