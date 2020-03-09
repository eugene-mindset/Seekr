from flask import Blueprint, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from app import mongo

items_router = Blueprint("items", __name__)

@items_router.route("/")
def hello():
    return "Hello World!"

@items_router.route('/items', methods=['GET'])
def get_all_items():
    items = mongo.db.items

    output = []
    for item in items.find():
        output.append({'id': str(item['_id']), 'name' : item['name'], 'found': item['found'], 'desc': item['desc']})

    return jsonify(output), 200

@items_router.route('/items/<name>', methods=['GET'])
def get_item(name):
    items = mongo.db.items
    output = []

    for item in items.find({"name" : name}):
        output.append({'id': str(item['_id']), 'name' : item['name'], 'found': item['found'], 'desc': item['desc']}) 

    return jsonify(output), 200

@items_router.route('/items', methods=['POST'])
def add_item():
    items = mongo.db.items

    name = request.get_json()['name']
    found = request.get_json()['found']
    desc = request.get_json()['desc']

    item_id = items.insert({'name' : name, 'found': found, 'desc':desc})
    new_item = items.find_one({'_id' : item_id})

    output = {'id': str(new_item['_id']), 'name' : new_item['name'], 'found': found, 'desc': new_item['desc']}

    return jsonify(output), 200

@items_router.route('/items/<id>', methods=['PUT'])
def update_item(id):
    items = mongo.db.items

    name = request.get_json()['name']
    found = request.get_json()['found']
    desc = request.get_json()['desc']

    items.find_one_and_update({'_id':ObjectId(id)}, {"$set": {"name": name, 'found': found, 'desc': desc}}, upsert=False)
    item = items.find_one({'_id' : ObjectId(id)})
    output = {'id': str(item['_id']), 'name' : item['name'], 'found': found, 'desc': item['desc']}

    return jsonify(output), 200

@items_router.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    items = mongo.db.items

    returned = items.delete_one({'_id': ObjectId(id)})

    if returned.deleted_count == 1:
        output = {'message': 'deleted'}
    else:
        output = {'message': 'not deleted'}

    return jsonify({'result' : output}), 200