from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from app.models.models import *
from app import mongo

items_router = Blueprint("items", __name__)

@items_router.route("/")
def hello():
    return "Hello World!"

@items_router.route('/items', methods=['GET'])
def get_all_items():
    items = mongo.db.items
    itemObj = ItemDao(items)
    output = itemObj.findByName()
    return jsonify(output), 200

@items_router.route('/items/<name>', methods=['GET'])
def get_item(name):
    items = mongo.db.items
    itemObj = ItemDao(items)
    output = itemObj.findByName(name)
    return jsonify(output), 200

@items_router.route('/items', methods=['POST'])
def add_item():
    items = mongo.db.items

    name = request.get_json()['name']
    found = request.get_json()['found']
    desc = request.get_json()['desc']

    items = mongo.db.items
    itemObj = ItemDao(items)
    output = itemObj.insert(name, found, desc)
    return jsonify(output), 200

@items_router.route('/items/<id>', methods=['PUT'])
def update_item(id):
    items = mongo.db.items

    name = request.get_json()['name']
    found = request.get_json()['found']
    desc = request.get_json()['desc']

    itemObj = ItemDao(items)
    output = itemObj.update(id, name, found, desc)
    return jsonify(output), 200

@items_router.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    items = mongo.db.items
    itemObj = ItemDao(items)
    numDeleted = itemObj.remove(id)

    if numDeleted == 1:
        output = {'message': 'deleted'}
    else:
        output = {'message': 'not deleted'}

    return jsonify({'result' : output}), 200