import docker
from docker.models.images import Image
from pathlib import Path

from app.models.project import Project
from app.services.containerizer.instance import ProjectInstance


ROOT = Path("/home/sasho_b/Coding/cob/docker")
DOCKER_TEMPLATE = Path(ROOT, "dockerfile_template")
CLIENT = docker.from_env()


def fillout_template(p: Project) -> None:
    template = ''
    entry_file = Path(p.entry_file)

    with open(DOCKER_TEMPLATE, 'r') as file:
        template = file.read()
        template = template.replace('{entry_file}', entry_file.name)

    with open(Path(p.source_dir,"Dockerfile"), "w+") as save_to:
        save_to.write(template)


def create_detached_instance(p: Project):
    fillout_template()

    image = CLIENT.images.build(path=str(p.source_dir), rm=True)[0] # rm=True OR IT BREAKS!

    container = CLIENT.containers.create(image.id)
    instance = ProjectInstance(container)
    instance.start()

    image.remove(force=True)

    return instance.id


if __name__ == '__main__':
    p = Project('/home/sasho_b/Coding/debug_cob/main.py', '/home/sasho_b/Coding/debug_cob')
    id = create_detached_instance(p)
    print(id)
