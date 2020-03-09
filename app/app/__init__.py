from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS



app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'mydb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mongotask'

CORS(app)
mongo = PyMongo(app)

def create_app():
    register_blueprints(app)
    return app

def register_blueprints(application):
    from app.controllers import items_router
    application.register_blueprint(items_router)