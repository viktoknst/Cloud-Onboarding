
class Instance:
    pass


# cass which runs containers and saves their results to MongoDB
# takes a template Dockerfile and fills it out


# configures a project and executes it, then cleans up
def run_project(entry_file: Path,source_dir: Path,build_dir: Path | None = None,):
    if build_dir == None:
        build_dir = source_dir
    fillout_template(entry_file, source_dir, build_dir)
    return result

if __name__ == "__main__":
    source_dir = Path("/home/sasho_b/Coding/cob/user")
    entry_point = Path(source_dir, "hello.py")
    result = run_project(entry_point, source_dir)
    print(result)
    print("Done")

user->project->compiled_project(image)->running_instance(container)

def build_project(p: Project):
    prepare_project_dir
    build_image

def start_project(p: Project):
    build_container

def delete_project(p: Project):

def project_output_to_db(entry_file: Path, source_dir: Path, id: uuid.UUID) -> None:
    DBInterface.save_result({'uuid': str(id), "status": "running"})
    result = ContainerManager.run_project(entry_file, source_dir)
    print(DBInterface.results.update_one({'uuid': str(id)}, {"$set":{"status": "done", "result": result}}))

# runs a project in a separate thread. returns an identifier for retrieval
def run_project_detached(user: str, project: str) -> uuid.UUID:
    id = uuid.uuid4()
    entry_file = get_project_entry_file(user, project)
    thread = Thread(target=project_output_to_db, args=[entry_file, Path(user_manager.get_user_dir(user), project), id])
    thread.daemon = False
    thread.start()
    thread.join()
    return id
