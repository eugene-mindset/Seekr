from flask import Blueprint, jsonify, request, send_from_directory, send_file
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from app.models.models import *
from app.controllers.tags import *
from app import mongo
from app.models.similarity import ItemSimilarity
import os
import gensim.downloader as gens_api

items_router = Blueprint("items", __name__)


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


@items_router.route("/")
def hello():
    return "Hello World"

@items_router.route("/fetch_image/<filename>")
def fetch_resource(filename):
    print("THIS IS THE FILENAME"+ filename)
    return send_from_directory('../'+IMAGE_FOLDER, filename)

@items_router.route('/items', methods=['GET'])
def get_all_items():
    items = mongo.db.items
    itemObj = ItemDao(items)
    
    # Get any arguments in the query
    args = request.args
    
    # Get the tags if exists
    tags = []
    if (args.get('tags') != None):
        tags = args.get('tags').split(',')
        
    listOfItems = itemObj.findAll(tags)
    output = []
    for i in listOfItems:
        output.append(i.toDict())
    return jsonify(output), 200


@items_router.route('/items/<query>', methods=['GET'])
def get_all_items_sorted(query):
    items = mongo.db.items
    itemObj = ItemDao(items)
    
    # Get any arguments in the query
    args = request.args
    
    # Get the tags if exists
    tags = []
    if (args.get('tags') != None):
        tags = args.get('tags').split(',')
        
    listOfItems = itemObj.findAll(tags)
    queriedItem = Item(name=query, desc="")

    simMatch = ItemSimilarity(modelName=None)
    simMatch.model = embedding

    simMatch.addItems(listOfItems)
    simMatch.computeBagOfWordsForItems()
    simMatch.computeSimilarityMatrix()
    simMatch.scoreItems(queriedItem, True, True)

    output = [item.toDict() for item in simMatch.getSortedItems()]
    return jsonify(output)


# DEPRECATED
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

    items = mongo.db.items
    name = request.form['name']
    found = eval(request.form['found'].capitalize())
    desc = request.form['desc']
    location = request.form['location']
    imageName = f.filename if f != None else ''
    tags = request.form['tags']
    
    items = mongo.db.items
    itemObj = ItemDao(items)
    item = Item(name=name, found=found, desc=desc, location=location, imageName=imageName, tags=tags)

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
