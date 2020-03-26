from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from app.models.models import *
from app.controllers.tags import *
from app import mongo

items_router = Blueprint("items", __name__)

# tags:
#   tech
#   clothing
#   jewelry
#   pet
#   personal - wallets, keys, id's
#   apparel - clothing, accessories, purse
#   other - anything not in the above categories: bikes, coffee mugs, etc

@items_router.route("/")
def hello():
    return "Hello World!"


@items_router.route('/items', methods=['GET'])
def get_all_items():
    items = mongo.db.items
    itemObj = ItemDao(items)
    listOfItems = itemObj.findAll()
    output = []
    for i in listOfItems:
        output.append(i.toDict())
    return jsonify(output), 200


@items_router.route('/items/search=<query>', methods=['GET'])
def get_all_items_sorted(query):
    items = mongo.db.items
    itemObj = ItemDao(items)
    listOfItems = itemObj.findAll()

    queriedItem = Item(name=query, desc="")
    scoredItems = [(queriedItem.compareItem(item), item) for item in listOfItems]
    scoredItems.sort(key=lambda tup: tup[0], reverse=True)

    output = [pair[1].toDict() for pair in scoredItems]

    return jsonify(output)


@items_router.route('/items/<name>', methods=['GET'])
def get_item(name):
    items = mongo.db.items
    itemObj = ItemDao(items)
    output = []
    listOfItems = itemObj.findByName(name)
    for i in listOfItems:
        output.append(i.toDict())
    return jsonify(output), 200


@items_router.route('/items', methods=['POST'])
def add_item():
    items = mongo.db.items

    name = request.get_json()['name']
    found = request.get_json()['found']
    desc = request.get_json()['desc']
    location = request.get_json()['location']
    tags = request.get_json()['tags']
    
    items = mongo.db.items
    itemObj = ItemDao(items)
    item = Item(name=name, found=found, desc=desc, location=location, tags=tags)
    itemObj.insert(item)
    return jsonify(item.toDict()), 200


@items_router.route('/items/<id>', methods=['PUT'])
def update_item(id):
    items = mongo.db.items

    name = request.get_json()['name']
    found = request.get_json()['found']
    desc = request.get_json()['desc']
    location = request.get_json()['location']
    tags = request.get_json()['tags']
    
    itemObj = ItemDao(items)
    item = Item(Id=id, name=name, found=found, desc=desc, location=location, tags=tags)
    itemObj.update(item)
    return jsonify(item.toDict()), 200


@items_router.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    items = mongo.db.items
    itemObj = ItemDao(items)
    numDeleted = itemObj.remove(id)

    if numDeleted == 1:
        output = {'message': 'deleted'}
    else:
        output = {'message': 'not deleted'}

    return jsonify({'result': output}), 200
