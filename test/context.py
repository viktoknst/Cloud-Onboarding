# include in all tests:
#
#from context import src
#from context import config
#
#import pytest
#from unittest.mock import patch
#
#from src import myfile

import os
import sys
# black magic that makes the test workdir test/..
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src
import src.config as config
