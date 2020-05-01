from unittest import TestCase
from app.models import *
from config import TestConfig
from app import create_app
from app.mongo_inst import mongo
from flask_pymongo import MongoClient
import json

class UserTest(TestCase):

    def setUp(self):
        # Set up test database
        app = create_app(TestConfig)
        app.testing = True
        self.app = app.test_client()
        users = mongo.db.users
        mongo_user_dao = UserDao(users)

                #Insert items into database
        name = "Ben"
        email = "ben@gmail.com"
        optIn = "false"
        user = User(name=name, email=email, optIn=optIn)
        mongo_user_dao.insert(user)
        name = "Mike"
        email = "mike@gmail.com"
        optIn = "true"
        user = User(name=name, email=email, optIn=optIn)
        mongo_user_dao.insert(user)
        name = "Neil"
        email = "neil@gmail.com"
        optIn = "false"
        user = User(name=name, email=email, optIn=optIn)
        mongo_user_dao.insert(user)

    def tearDown(self):
        client = MongoClient('localhost', 27017)
        client.drop_database(TestConfig.MONGO_DBNAME)

    def test_get_all_users(self):
        response = self.app.get('/api/userinfo')
        response_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict), 3)
        item = response_dict[0]
        self.assertEqual(item['name'], "Ben")
        self.assertEqual(item['email'], "ben@gmail.com")
        self.assertEqual(item['optIn'], "false")
        item = response_dict[1]
        self.assertEqual(item['name'], "Mike")
        self.assertEqual(item['email'], "mike@gmail.com")
        self.assertEqual(item['optIn'], "true")
        item = response_dict[2]
        self.assertEqual(item['name'], "Neil")
        self.assertEqual(item['email'], "neil@gmail.com")
        self.assertEqual(item['optIn'], "false")

    def test_get_user__based_on_email(self):
        response = self.app.get('/api/userinfo/ben@gmail.com')
        response_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict), 1)
        self.assertEqual(response_dict[0]['name'], "Ben")
        
