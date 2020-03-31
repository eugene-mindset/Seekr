from flask import Blueprint, jsonify, request, send_from_directory, send_file
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from app.models.models import *
from app import mongo
import os

items_router = Blueprint("items", __name__)

IMAGE_FOLDER = os.path.dirname('uploadedImages/')

@items_router.route("/")
def hello():
    return "Hello World"

@items_router.route("/fetch_image/<filename>")
def fetch_resource(filename):
    return send_from_directory('../'+IMAGE_FOLDER, filename)

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

    # save image to local folder
    f = request.files['image']
    f.save(os.path.join(IMAGE_FOLDER, secure_filename(f.filename)))

    items = mongo.db.items

    name = request.form['name']
    found = request.form['found']
    desc = request.form['desc']
    location = request.form['location']
    imageName = request.files['image'].filename

    items = mongo.db.items
    itemObj = ItemDao(items)
    item = Item(name=name, found=found, desc=desc, location=location, imageName=imageName)
    itemObj.insert(item)
    return jsonify(item.toDict()), 200


@items_router.route('/items/<id>', methods=['PUT'])
def update_item(id):
    items = mongo.db.items

    name = request.get_json()['name']
    found = request.get_json()['found']
    desc = request.get_json()['desc']
    location = request.get_json()['location']

    itemObj = ItemDao(items)
    item = Item(Id=id, name=name, found=found, desc=desc, location=location)
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
