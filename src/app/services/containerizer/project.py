from pathlib import Path

import docker

from app.crud.project_crud import Project
from app.services.containerizer.instance import ProjectInstance


ROOT = Path("/home/sasho_b/Coding/cob/docker")
DOCKER_TEMPLATE = Path(ROOT, "dockerfile_template")
CLIENT = docker.from_env()


def fillout_template(p: Project) -> None:
    template = ''
    entry_file = Path(p.entry_file)

    with open(DOCKER_TEMPLATE, 'r', encoding='utf-8') as file:
        template = file.read()
        template = template.replace('{entry_file}', entry_file.name)

    with open(Path(p.source_dir,"Dockerfile"), "w+", encoding='utf-8') as save_to:
        save_to.write(template)


def create_detached_instance(p: Project, db):
    fillout_template(p)

    image = CLIENT.images.build(path=str(p.source_dir), rm=True)[0] # rm=True OR IT BREAKS!

    container = CLIENT.containers.create(image.id)
    instance = ProjectInstance(container, db)
    instance.start()

    image.remove(force=True)

    return instance.id

# OLD
#if __name__ == '__main__':
#    project = Project('/home/sasho_b/Coding/debug_cob/main.py', '/home/sasho_b/Coding/debug_cob')
#    id = create_detached_instance(project)
#    print(id)
