from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from .mongo_inst import mongo

app = Flask(__name__)


#Configure app from object input and enable CORS
def create_app(config_obj):
    app.config.from_object(config_obj)
    CORS(app)
    mongo.init_app(app)
    register_blueprints(app)
    return app

def register_blueprints(application):
    from app.controllers import items_router
    application.register_blueprint(items_router)
