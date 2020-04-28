from pathlib import Path

from flask import Blueprint, jsonify, request, send_from_directory, send_file
from app import mongo
from app.models.models import User, UserDao

users_router = Blueprint("user", __name__)

users = mongo.db.users # our items collection in mongodb
mongo_user_dao = UserDao(users) # initialize a DAO with the collection

@users_router.route('/api/userinfo', methods=['POST'])
def add_user():
    name = request.form['username']
    email = request.form['email']
    optIn = request.form['optIn']
    
    # Find a matching user
    matchingUser = mongo_user_dao.findAllMatchingEmail(email)
    
    # If a user already exists upon login, then don't create a new user
    if matchingUser:
        user = User(Id=matchingUser[0].Id, name=name, email=email, optIn=optIn)
        return jsonify(user.toDict()), 200
    
    user = User(name=name, email=email, optIn=optIn)

    mongo_user_dao.insert(user)

    return jsonify(user.toDict()), 200

@users_router.route('/api/userinfo', methods=['PUT'])
def update_user():
    name = request.form['username']
    email = request.form['email']
    optIn = request.form['optIn']
    print(optIn)
    matchingUser = mongo_user_dao.findAllMatchingEmail(email)

    user = User(Id=matchingUser[0].Id, name=name, email=email, optIn=optIn)

    mongo_user_dao.update(user)
    return jsonify(user.toDict()), 200

@users_router.route('/api/userinfo', methods=['GET'])
def get_all_users():
    # get list of all items using DAO and specifying the tags
    listOfUsers = mongo_user_dao.findAll()

    output = [user.toDict() for user in listOfUsers]
    return jsonify(output), 200