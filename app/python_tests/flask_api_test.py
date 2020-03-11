<<<<<<< HEAD:app/app/python_tests/flask_api_test.py
import unittest
from app import create_app
from app.mongo_inst import mongo
from app.models import *
from flask_pymongo import MongoClient, PyMongo
from config import *
import json

class ApiTest(unittest.TestCase):

    def setUp(self):
        app = create_app(TestConfig)
        app.testing = True
        self.app = app.test_client() 
        items = mongo.db.items
        itemObj = ItemDao(items)

        #Insert items already
        name = "pen"
        found = False
        desc = "It is a pen"
        item = Item(name = name, found = found, desc = desc)
        itemObj.insert(item)
        name = "card"
        found = True
        desc = "It is a card"
        item = Item(name = name, found = found, desc = desc)
        itemObj.insert(item)

    def tearDown(self):
        client = MongoClient('localhost', 27017)
        client.drop_database(TestConfig.MONGO_DBNAME)

    def test_get_all_item(self):
        response = self.app.get('/items')
        response_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict), 2)

    def test_get_all_items_sorted(self):
        response = self.app.get('/items/search=pen')
        response_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict), 2)
        self.assertEqual(response_dict[0]['name'], 'pen')

    def test_get_all_item(self):
        response = self.app.get('/items')
        response_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict), 2)
