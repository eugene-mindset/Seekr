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
        
    def test_add_new_user(self):
        data = {
            'username': 'Seek R',
            'email' : 'seekr.oose@gmail.com',
            'optIn' : 'false'
            }
        
        response = self.app.post(
            '/api/userinfo',
            data=data
        )
        
        response_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict), 6)
        self.assertEqual(response_dict['name'], "Seek R")
        self.assertEqual(response_dict['email'], "seekr.oose@gmail.com")
        self.assertEqual(response_dict['optIn'], "false")
        self.assertEqual(response_dict['isAdmin'], True)
        self.assertEqual(response_dict['listOfItemIds'], [])
        
    
    def test_add_existing_user(self):
        data = {
            'username': 'Ben',
            'email' : 'ben@gmail.com',
            'optIn' : 'false'
            }
        
        response = self.app.post(
            '/api/userinfo',
            data=data
        )
        
        response_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict), 6)
        self.assertEqual(response_dict['name'], "Ben")
        self.assertEqual(response_dict['email'], "ben@gmail.com")
        self.assertEqual(response_dict['optIn'], "false")
        self.assertEqual(response_dict['isAdmin'], False)
    
    # delete user
    def test_delete_user(self):
        data = {
            'username': 'Ben',
            'email' : 'ben@gmail.com',
            'optIn' : 'false'
            }
        
        response = self.app.post(
            '/api/userinfo',
            data=data
        )
        
        id = json.loads(response.data)['id']
        
        response = self.app.delete(
            '/api/userinfo/' + id,
            data=data
        )
        self.assertEqual(response.status_code, 200)

    # update user
    def test_update_user(self):
        data = {
            'username': 'Ben',
            'email' : 'ben@gmail.com',
            'optIn' : 'true'
            }
        
        response = self.app.put(
            '/api/userinfo',
            data=data
        )
        
        response_dict = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_dict), 6)
        self.assertEqual(response_dict['name'], "Ben")
        self.assertEqual(response_dict['email'], "ben@gmail.com")
        self.assertEqual(response_dict['optIn'], "true")
        self.assertEqual(response_dict['isAdmin'], False)
        
    # get user opt in is true
    def test_get_user_opt_in_True(self):

        response = self.app.get('/api/optin/mike@gmail.com')
        self.assertEqual(response.status_code, 200)
        response_dict = json.loads(response.data)
        self.assertEqual(len(response_dict), 1)
        self.assertEqual(response_dict[0], True)
    
    # get user opt in is false
    def test_get_user_opt_in_False(self):

        response = self.app.get('/api/optin/seekr.oose@gmail.com')
        self.assertEqual(response.status_code, 200)
        response_dict = json.loads(response.data)
        self.assertEqual(len(response_dict), 1)
        self.assertEqual(response_dict[0], False)