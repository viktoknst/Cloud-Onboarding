'''
File to ensure that tests are working.
'''

import context
import pytest

from app.special import test


def test_add_two_nums():
    '''
    Used for testing
    '''
    assert test.add_two_nums(1,2) == 3
    assert test.add_two_nums(6,-8.5) == -2.5
    with pytest.raises(Exception): # assert an exception is raised
        assert test.add_two_nums(1,2) == 4
    with pytest.raises(Exception):
        test.add_two_nums("Helo", None)
