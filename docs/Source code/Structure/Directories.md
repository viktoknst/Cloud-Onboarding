There are 6 directories under `src/app`. They are:
* `crud` - Folder for the creation, reading, update and deletion of resources. This folder is concerned with working with resources as they exist on the database and transform them into representations to be used by the rest of the code. Files in crud should be named `{resource}_crud.py`

* `routers` - Folder which contains FastAPI endpoints for both crud and any other HTTP logic. Each file in `app/routers` should create its own router, and add all relevant endpoints to that router. Files in routers/ should not import logic related to using external resources or dependencies.  Endpoint functions can only operate with files from
  `schemas`, `crud`, FastAPI and relevant HTTP, and implement dependencies via the `Depends()` function from FastAPI. The routers from these files are to be imported into `src/main.py` and added to the FastAPI object. More information [[Endpoints|here]].

* `schemas` - Data representations of resources as HTTP requests/responses (create, read, update, delete, may or may not overlap), called schemas. Schemas should implement `pydantic.BaseModel` and always have type annotations, as this is how FastAPI does type validation for requests.

* `external_dependencies` - DB, external services, anything outside of our control.

* `services` - Anything else. Intermediate classes, logic, system operations that do not concern the other things, etc.

* `special` -  Includes a dictionary of endpoints and the user directory. Also, it has a file to confirm that tests are working.
