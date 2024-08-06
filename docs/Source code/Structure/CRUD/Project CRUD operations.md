Module that handles CRUD operations for projects in the DB:

#### `class Project` -

Object representation of a user's project. Handles saving/reading from a db. Expects a mong-like db interface.

#### `def set_db(cls, db: Database)`-

Sets the database to be used by the class and all its instances.
Args:
* db (Database): A mongo-like db

#### `def create(cls, user: User, name: str)` -

Creates a project in db and file system.
Returns the resulting project object.

Args:
*  user (User): The owner to create said project
*  name (str): The project name

Raises:
*  Exception: Project name is invalid\n
*  Exception: User has project of the same name\n
*  Exception: Project dir already exists

Returns:
*  Project: The resulting project object

#### `def read(cls, user: User, id: str | None = None, name: str | None = None)` -

Reads a project from db.
Requires the owner and either project id or proejct name.
If neither are provided, throws an exception.
If the project doesnt exist, throws an exception.

Args:
*  user (User): Owner of the project
*  id (str | None, optional): Project id. Defaults to None.
*  name (str | None, optional): Project name. Defaults to None.

Raises:
*  ValueError: No identifying arguments provided
*  ValueError: The project was not found

Returns:
*  Project: The project from the db

#### `def update(self)` -

Saves the current state of the object (fields) to the db.
Some fields that should not be altered are not saved.

#### `def delete(self)` -

Deletes project from database and the file system.
Does not alter the object itself.

#### `def add_file(self, file: BinaryIO, filename: str, is_entry: bool)` -

Adds a file to the file directory.
If another file of the same name exists - overwrites it.
If `is_entry` is set to true, the file is set as the project entry point.
Updates the project in db accordingly.

Args:
*  file (BinaryIO): The file data in binary
*  filename (str): The name to write to
*  is_entry (bool): Is project entry point
