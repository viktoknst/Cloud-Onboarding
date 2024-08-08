Module that handles CRUD operations for users in the DB

#### `class User` -

Object representation of a user's project.
Handles saving/reading from a db.
Expects a mong-like db interface.

#### `def set_db(cls, db: Database)` -

Sets the database to be used by the class and all its instances.

Args:
*  db (Database): A mongo-like db

#### `def create(cls, name: str, password: str)` -

Creates a user in db and file system.
Returns the resulting user object.

Args:
*  name (str): User
*  password (str): User password

Raises:
*  ValueError: User name is invalid\n
*  ValueError: Password is invalid\n
*  ValueError: User name is in use\n
*  Exception: User directory is in use/already exist

Returns:
*  User: The resulting user object

#### `def read(cls, id: str | None = None, name: str | None = None)` -

Reads a user from db.
Requires either user id or user name.
If neither are provided, throws an exception.
If the user doesnt exist, throws an exception.

Args:
*  id (str | None, optional): User id. Defaults to None.
*  name (str | None, optional): User name. Defaults to None.

Raises:
*  ValueError: No identifying arguments provided
*  ValueError: The user was not found

Returns:
*  User: The user from the db

#### `def update(self)` -

Saves the current state of the object (fields) to the db.
Some fields that should not be altered are not saved.

#### `def delete(self)` -

Deletes project from database and the file system.
Does not alter the object itself.
If deleting from FS failed, throws exception but still deletes from db.

Raises:
*  Exception: On user dir removal failure

#### `def change_password(self, new_password: str)` -

Changes the user password.
Validates it, generates new salt+hash.
Must `.update()` for change to take effect.

Args:
*  new_password (str): The new password.

Raises:
*  ValueError: Invalid password
