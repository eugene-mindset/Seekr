from base64 import standard_b64encode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import math
import os
import smtplib
import ssl
import time

from flask import Blueprint, jsonify, request, send_from_directory, send_file
from flask_pymongo import PyMongo
import gensim.downloader as gens_api
from werkzeug.utils import secure_filename

from app import mongo
from app.controllers.notifications import *
from app.models.models import *
from app.models.similarity import ItemSimilarity


items_router = Blueprint("items", __name__)

embedding = gens_api.load('glove-wiki-gigaword-50')
items = mongo.db.items # our items collection in mongodb
mongo_item_dao = ItemDao(items) # initialize a DAO with the collection


@items_router.route("/")
def hello():
    return "Hey! You're not supposed to be here!"


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

@items_router.route('/items/proximitysearch=<query>', methods=['GET'])
def get_all_items_proximitysorted(query):
    # Get the tags if provided
    tags = ItemTags.get(request.args.get('tags'))
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    # get list of all items using DAO and specifying the tags
    listOfItems = mongo_item_dao.findAll(tags)

    #Calculate distance between objects
    distItems = []
    for item in listOfItems:
        R = 6373.0
        lat1 = math.radians(float(lat))
        lon1 = math.radians(float(lon))
        lat2 = math.radians(float(item.location.coordinates[0]))
        lon2 = math.radians(float(item.location.coordinates[1]))

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        item.distance = distance
        distItems.append(item)
        print(item.name + " " + str(item.distance))

    # sort items by most recently added (higher timestamp)
    distItems.sort(key=lambda x: x.distance, reverse=False)

    #output = [pair[1].toDict() for pair in scoredItems]
    output = [item.toDict() for item in distItems]

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


@items_router.route('/items', methods=['POST'])
def add_item():

    name = request.form['name']
    desc = request.form['desc']
    found = request.form['found'] == 'True'
    location = Location([float(request.form['latitude']),
                         float(request.form['longitude'])])
    radius = float(request.form['radius'])
    tags = ItemTags.get(request.form['tags'])
    
    # Get the list of uploaded images and convert them to ItemImage objects
    uploadedImages = request.files.getlist('image')
    images = []
    for img in uploadedImages:
        encoded = standard_b64encode(img.read())
        encodedAsStr = encoded.decode()
        images.append(ItemImage(img.filename, img.mimetype, encodedAsStr))

    timestamp = time.time()
    user = User(request.form['username'], request.form['email'],
                request.form['phone'])

    item = Item(name=name, desc=desc, found=found, location=location,
                radius=radius, tags=tags, images=images,
                timestamp=timestamp, user=user, distance=0.0)

    mongo_item_dao.insert(item)

    # Check if added item is similar to any current items, if so then send notification
    notify(item)

    return jsonify(item.toDict()), 200


@items_router.route('/items/<Id>', methods=['PUT'])
def update_item(Id):
    # TODO: Update this to match the new architecture of objects
    # Actually let the user update items on the frontend

    name = request.form['name']
    desc = request.form['desc']
    found = request.form['found'] == 'True'
    location = Location([float(request.form['latitude']),
                         float(request.form['longitude'])])
    radius = float(request.form['radius'])
    tags = ItemTags.get(request.form['tags'])
    user = User(request.form['username'], request.form['email'],
                request.form['phone'])

    item = Item(Id=Id, name=name, desc=desc, found=found, location=location,
                radius=radius, tags=tags, user=user, distance=0.0)

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
