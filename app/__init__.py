from flask import Flask, jsonify, request
#from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
from .mongo_inst import mongo

app = Flask(__name__)


def create_app(config_obj):
    """Creates the flask application and enables CORS

    Creates the flask application from an object with the MongoDB name and URI.\n
    Enables Cross-Origin Resource Sharing (CORS) to allow access to resources
    from a different origin.

    Args:
        config_obj: configuration object

    Returns:
        The configured flask app.
    """

    app.config.from_object(config_obj)
    CORS(app)
    mongo.init_app(app)
    register_blueprints(app)
    return app


def register_blueprints(application):
    """Registers a Blueprint on the application. A Blueprint is a collection of
    routes and other app functions.

    Args:
        application: The flask application to register the Blueprint on.
    """

    from app.controllers import items_router
    from app.controllers import users_router
    application.register_blueprint(items_router)
    application.register_blueprint(users_router)