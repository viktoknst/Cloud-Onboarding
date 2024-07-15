There are 6 directories under `src/app`. They are:
* crud - for the creation, reading, update and deletion of resources. Used for resources with crud only, or as a forward for resources with inside logic.
* routers - files with fastapi endpoints for both crud and any other http task
* models - data representations of resouces as they are in the db. May be used by logic classes but should not be using a DB explicitly
* schemas - data representations of resources as requests (create, read, update, delete, may or may not overlap)
* external_dependencies - db, services, anything outside of our controll
* services - anything else. intermediete classes, logic, system operations that dont concern the other things, etc
