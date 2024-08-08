from pathlib import Path

import docker

from app.crud.project_crud import Project
from app.services.containerizer.instance import ProjectInstance

CLIENT = docker.from_env()


def create_detached_instance(p: Project):
    image = CLIENT.images.get("python")

    container = CLIENT.containers.create(
        image.id,
        command=f"python /src/{p.entry_file}",
        volumes={p.source_dir: {'bind': '/src', 'mode': 'ro'}}
    )
    instance = ProjectInstance(container)
    return instance

# OLD
#if __name__ == '__main__':
#    project = Project('/home/sasho_b/Coding/debug_cob/main.py', '/home/sasho_b/Coding/debug_cob')
#    id = create_detached_instance(project)
#    print(id)
