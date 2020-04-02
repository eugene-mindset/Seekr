#BC of pythons terrible importing
#coverage run --source=./ run_tests.py
from app import create_app
from app.python_tests.flask_api_test import *
from app.python_tests.similarity_test import *
import unittest

#Run the tests
unittest.main()
