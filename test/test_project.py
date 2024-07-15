from context import src
from context import config

import pytest
from unittest.mock import patch

from src.models import project

project.Project().create_detached_instance()
