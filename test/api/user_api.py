from context import src
import pytest
from unittest.mock import patch

import src.api.user_api as user_api

# spoof function to replace mkdir
def mock_mkdir(path, mode=0o777, *, dir_fd=None):
    print(f"Mock mkdir called with: path={path}, mode={mode}, dir_fd={dir_fd}")

def test_post_create_user():
    valid = user_api.UserCreationRequest(user_name="john_doe")
    invalid = user_api.UserCreationRequest(user_name="john_dWZ%sk6ejyrnstgafvdasoe")

    with patch('os.mkdir', new=mock_mkdir):
        assert user_api.post_create_user(valid)

    with pytest.raises(Exception) as ex:
        user_api.post_create_user(invalid)
