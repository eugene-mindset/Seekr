import unittest
from app import create_app
from app.mongo_inst import mongo
from app.models import *
from flask_pymongo import MongoClient, PyMongo
from config import *
import json


class ApiTest(unittest.TestCase):

    def setUp(self):
        # Set up test database
        app = create_app(TestConfig)
        app.testing = True
        self.app = app.test_client()
        items = mongo.db.items
        mongo_item_dao = ItemDao(items)

        #Insert items into database
        name = "Pen"
        found = False
        desc = "It is a pen"
        item = Item(name=name, found=found, desc=desc)
        mongo_item_dao.insert(item)
        name = "Card"
        found = True
        desc = "It is a card"
        item = Item(name=name, found=found, desc=desc)
        mongo_item_dao.insert(item)
        name = "Phone"
        found = True
        desc = "It is a phone"
        item = Item(name=name, found=found, desc=desc)
        mongo_item_dao.insert(item)

    def tearDown(self):
        client = MongoClient('localhost', 27017)
        client.drop_database(TestConfig.MONGO_DBNAME)

    def test_get_all_item(self):
        response = self.app.get('/items?tags=0')
        response_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict), 3)
        item = response_dict[0]
        self.assertEqual(item['name'], 'Pen')
        self.assertEqual(item['found'], False)
        self.assertEqual(item['desc'], 'It is a pen')
        item = response_dict[1]
        self.assertEqual(item['name'], 'Card')
        self.assertEqual(item['found'], True)
        self.assertEqual(item['desc'], 'It is a card')

    def test_get_all_items_sorted(self):
        response = self.app.get('/items/search=pen?tags=0')
        response_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict), 3)
        self.assertEqual(response_dict[0]['name'], 'Pen')
