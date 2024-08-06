Module that handles CRUD operations for results in the DB

#### `class Result` -

Object representation of the result from running a project.
Handles saving/reading from a db.

#### `def set_db(cls, db: Database)` -

Sets the database to be used by the class and all its instances.

Args:
*  db (Database): A mongo-like db

#### `def create(cls, result: str | None)` -

Creates result into the given DB.
Result is created as 'running' by default

Args:
*  db (Database): _description_
*  id (str): _description_

#### `def read(cls, id: str)` -

Reads given result from the given DB.

Args:
*  db (Database): _description_
*  result_id (str): _description_

Returns:
*  Result: _description_

#### `def update(self)` -

Saves the current state of the object (fields) to the db.
Some fields that should not be altered are not saved.

#### `def delete(self)` -

Deletes result from database and the file system.
Does not alter the object itself.
