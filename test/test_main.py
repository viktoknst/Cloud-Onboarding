from context import src
import pytest

import src.main as main


def test_add_two_nums():
    assert main.add_two_nums(1,2) == 3
    assert main.add_two_nums(6,-8.5) == -2.5
    with pytest.raises(Exception) as ex: # assert an exception is raised
        assert main.add_two_nums(1,2) == 4
    with pytest.raises(Exception) as ex:
        main.add_two_nums("Helo", None)

if __name__ == '__main__':
    test_add_two_nums()
