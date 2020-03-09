import unittest
from app import create_app
class ApiTest(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_hello(self):
        self.assertEqual(1, 1)
