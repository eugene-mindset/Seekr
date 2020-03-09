import unittest
from app import create_app
class ApiTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app = self.app.test_client() 
    def tearDown(self):
        pass
    def test_get_all_item(self):
        response = self.app.get('/items')
        print(response.data)
        self.assertEqual(response.status_code, 200)
