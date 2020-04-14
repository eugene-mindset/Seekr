from flask import Blueprint, jsonify, request, send_from_directory, send_file
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from app.models.models import *
from app import mongo
from app.models.similarity import ItemSimilarity
import os
import gensim.downloader as gens_api
import time

items_router = Blueprint("items", __name__)

# TODO: do we really need this here? delete at some point
# tags:
#   tech
#   clothing
#   jewelry
#   pet
#   personal - wallets, keys, id's
#   apparel - clothing, accessories, purse
#   other - anything not in the above categories: bikes, coffee mugs, etc

IMAGE_FOLDER = os.path.dirname('uploadedImages/')
embedding = gens_api.load('glove-wiki-gigaword-50')
items = mongo.db.items # our items collection in mongodb
mongo_item_dao = ItemDao(items) # initialize a DAO with the collection


@items_router.route("/")
def hello():
    return "Hey! You're not supposed to be here!"


@items_router.route("/fetch_image/<filename>")
def fetch_resource(filename):
    print("THIS IS THE FILENAME"+ filename)
    return send_from_directory('../'+IMAGE_FOLDER, filename)


@items_router.route('/items', methods=['GET'])
def get_all_items():
    # Get the tags if provided
    tags = ItemTags.get(request.args.get('tags'))

    # get list of all items using DAO and specifying the tags
    listOfItems = mongo_item_dao.findAll(tags)
    
    output = [item.toDict() for item in listOfItems]
    return jsonify(output), 200


@items_router.route('/items/timesearch=<query>', methods=['GET'])
def get_all_items_timesorted(query):
    # Get the tags if provided
    tags = ItemTags.get(request.args.get('tags'))

    # get list of all items using DAO and specifying the tags
    listOfItems = mongo_item_dao.findAll(tags)

    # sort items by most recently added (higher timestamp)
    listOfItems.sort(key=lambda x: x.timestamp, reverse=True)

    #output = [pair[1].toDict() for pair in scoredItems]
    output = [item.toDict() for item in listOfItems]

    return jsonify(output), 200


@items_router.route('/items/search=<query>', methods=['GET'])
def get_all_items_sorted(query):
    # Get the tags if exists
    tags = ItemTags.get(request.args.get('tags'))

    # get list of all items using DAO and specifying the tags
    listOfItems = mongo_item_dao.findAll(tags)

    # if nothing in db, don't do any similarity comparisons
    if not listOfItems:
        return jsonify([]), 200

    queriedItem = Item(name=query, desc="")

    simMatch = ItemSimilarity(modelName=None)
    simMatch.model = embedding
    simMatch.addItems(listOfItems)
    simMatch.scoreItems(queriedItem)

    output = [item.toDict() for item in simMatch.getSortedItems()]

    return jsonify(output), 200


# DEPRECATED TODO: delete this at some point
# @items_router.route('/items/<name>', methods=['GET'])
# def get_item(name):
#     items = mongo.db.items
#     itemObj = ItemDao(items)
#     output = []
#     # Get any arguments in the query
#     args = request.args
#     # Get the tags if exists
#     tags = []
#     if (args.get('tags') != None):
#         tags = args.get('tags').split(',')
#     listOfItems = itemObj.findByName(name, tags)
#     for i in listOfItems:
#         output.append(i.toDict())
#     return jsonify(output), 200

@items_router.route('/items', methods=['POST'])
def add_item():
    
    f = None
    # save image to local folder
    if 'image' in request.files:
        f = request.files['image']
        # Use secure_filename secure_filename(f.filename)
        f.save(os.path.join(IMAGE_FOLDER, f.filename))

    name = request.form['name']
    desc = request.form['desc']
    found = eval(request.form['found'].capitalize())
    location = Location([float(request.form['latitude']),
                        float(request.form['longitude'])])
    radius = float(request.form['radius'])
    tags = ItemTags.get(request.form['tags'])
    imageName = f.filename if f != None else ''
    timestamp = time.time()

    # TODO: placeholder, change this once user is handled on frontend
    user = User(name="Anderson", email="aadon1@jhu.edu", phone="555-555-5555")

    item = Item(name=name, desc=desc, found=found, location=location,
                radius=radius, tags=tags, imageName=imageName,
                timestamp=timestamp, user=user)

    mongo_item_dao.insert(item)
    return jsonify(item.toDict()), 200


@items_router.route('/items/<Id>', methods=['PUT'])
def update_item(Id):

    name = request.form['name']
    desc = request.form['desc']
    found = eval(request.form['found'].capitalize())
    location = Location([float(request.form['latitude']),
                        float(request.form['longitude'])])
    radius = float(request.form['radius'])
    tags = ItemTags.get(request.form['tags'])

    # TODO: placeholder, change this once user is handled on frontend
    user = User(name="Anderson", email="aadon1@jhu.edu", phone="555-555-5555")

    item = Item(Id=Id, name=name, desc=desc, found=found, location=location,
                radius=radius, tags=tags, user=user)

    mongo_item_dao.update(item)
    return jsonify(item.toDict()), 200


@items_router.route('/items/<Id>', methods=['DELETE'])
def delete_item(Id):
    numDeleted = mongo_item_dao.remove(Id)

    if numDeleted == 1:
        output = {'message': 'deleted'}
    else:
        output = {'message': 'not deleted'}

    return jsonify({'result': output}), 200
