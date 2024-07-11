from context import src
from context import config

import pytest
from unittest.mock import patch

import src.api.user_api as user_api

# spoof function to replace mkdir
def mock_mkdir(path, mode=0o777, *, dir_fd=None):
    print(f"Mock mkdir called with: path={path}, mode={mode}, dir_fd={dir_fd}")

def mock_path_exists_true(path: str):
    return True

def mock_path_exists_false(path: str):
    return False

def test_post_create_user():
    with patch('os.mkdir', new=mock_mkdir):
        valid = user_api.UserCreationRequest(user_name="john_doe")
        invalid = user_api.UserCreationRequest(user_name="john_dWZ%sk6ejyrnstgafvdasoe")

        # Fails
        with pytest.raises(Exception) as ex:
            user_api.post_create_user(invalid)

        # Works
        with patch('os.path.exists', new=mock_path_exists_false):
            user_api.post_create_user(valid)

        # Fails
        with patch('os.path.exists', new=mock_path_exists_true), pytest.raises(Exception) as ex:
            user_api.post_create_user(valid)

if __name__ == "__main__":
    test_post_create_user()
