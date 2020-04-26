from pathlib import Path

from flask import Blueprint, jsonify, request, send_from_directory, send_file
#from flask_pymongo import PyMongo
from app import mongo
from app.models.models import User, UserDao

users_router = Blueprint("user", __name__)

users = mongo.db.users # our items collection in mongodb
mongo_user_dao = UserDao(users) # initialize a DAO with the collection

@items_router.route('/userinfo', methods=['POST'])
def add_user():

    name = request.form['name']
    email = request.form['email']
    optIn = request.form['optIn']
    
    # Get the list of uploaded images and convert them to ItemImage objects

    user = User(request.form['username'], request.form['email'], request.form['optIn'])

    mongo_user_dao.insert(user)

    return jsonify(item.toDict()), 200

@items_router.route('/userinfo/<Id>', methods=['PUT'])
def update_user(Id):
    # TODO: Update this to match the new architecture of objects
    # Actually let the user update items on the frontend

    name = request.form['name']
    email = request.form['email']
    optIn = request.form['optIn']

    user = User(request.form['username'], request.form['email'], request.form['optIn'])


    mongo_item_dao.update(user)
    return jsonify(item.toDict()), 200