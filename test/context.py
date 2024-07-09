import os
import sys
# black magic that makes the test workdir test/..
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src
