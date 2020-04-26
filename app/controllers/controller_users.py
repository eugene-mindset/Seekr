from pathlib import Path

from flask import Blueprint, jsonify, request, send_from_directory, send_file
#from flask_pymongo import PyMongo
from app import mongo
from app.models.models import User, UserDao

users_router = Blueprint("user", __name__)

users = mongo.db.users # our items collection in mongodb
mongo_user_dao = UserDao(users) # initialize a DAO with the collection

@users_router.route('/userinfo', methods=['POST'])
def add_user():

    name = request.form['username']
    email = request.form['email']
    optIn = request.form['optIn']
    
    # Get the list of uploaded images and convert them to ItemImage objects

    user = User(name=name, email=email, optIn=optIn)

    mongo_user_dao.insert(user)

    return jsonify(user.toDict()), 200

@users_router.route('/userinfo/<Id>', methods=['PUT'])
def update_user(Id):
    # TODO: Update this to match the new architecture of objects
    # Actually let the user update items on the frontend

    name = request.form['username']
    email = request.form['email']
    optIn = request.form['optIn']

    user = User(name=name, email=email, optIn=optIn)

    mongo_item_dao.update(user)
    return jsonify(user.toDict()), 200

@users_router.route('/userinfo', methods=['GET'])
def get_all_users():
    # get list of all items using DAO and specifying the tags
    listOfUsers = mongo_user_dao.findAll()

    output = [user.toDict() for user in listOfUsers]
    return jsonify(output), 200