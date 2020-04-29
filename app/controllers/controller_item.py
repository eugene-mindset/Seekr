import math

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from time import time as currTime

from pathlib import Path

from flask import Blueprint, jsonify, request, send_from_directory, send_file
#from flask_pymongo import PyMongo

from gensim.models.keyedvectors import Word2VecKeyedVectors as word2vec
import gensim.downloader as gens_api

from app import mongo
from app.models.models import Item, ItemDao, ItemImage, ItemLocation, ItemTags, User, UserDao
from app.controllers.notifications import getSimItems, sendMail
from app.models.similarity import ItemSimilarity

items_router = Blueprint("items", __name__)

users = mongo.db.users
mongo_user_dao = UserDao(users)
items = mongo.db.items # our items collection in mongodb
mongo_item_dao = ItemDao(items) # initialize a DAO with the collection

# Location of where images for items are stored
IMAGE_FOLDER = Path('./uploadedImages/')

# the name of the model for item similarity to download
# for more models: https://github.com/RaRe-Technologies/gensim-data
simModelName = 'glove-wiki-gigaword-50'
simModel = None

# Load in the proper gensim files
modelLocation = Path('./sim_model_encoding')

if modelLocation.exists():
    # if the file exists, load that file
    # there should be two files, 'sim_model_encoding' and the same but with an
    # extension of vectors.npy
    print(' * Loading model from local')
    simModel = word2vec.load(str(modelLocation))
else:
    # get the gensim model from online and save it for future use if
    # there is no file
    print(' * Loading model remotely')
    simModel = gens_api.load(simModelName)
    simModel.save(str(modelLocation))


@items_router.route("/api/")
def hello():
    return "This is the API for the Seekr App!"


@items_router.route('/api/items', methods=['GET'])
def get_all_items():
    # Get the tags if provided
    tags = ItemTags.get(request.args.get('tags'))

    # get list of all items using DAO and specifying the tags
    listOfItems = mongo_item_dao.findAll(tags)

    output = [item.toDict() for item in listOfItems]
    return jsonify(output), 200


@items_router.route('/api/items/timesearch=<query>', methods=['GET'])
def get_all_items_timesorted(query):
    # Get the tags if provided
    tags = ItemTags.get(request.args.get('tags'))

    listOfItems = mongo_item_dao.findByMostRecent(tags, query)

    output = [item.toDict() for item in listOfItems]
    return jsonify(output), 200

@items_router.route('/api/items/all', methods=['GET'])
def get_all_items_recent():
    # Get the tags if provided
    tags = ItemTags.get(request.args.get('tags'))

    listOfItems = mongo_item_dao.findByMostRecent(tags)

    output = [item.toDict() for item in listOfItems]
    return jsonify(output), 200

@items_router.route('/api/items/proximitysearch', methods=['GET'])
def get_all_items_proximitysorted():
    # Get the tags if provided
    tags = ItemTags.get(request.args.get('tags'))
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    listOfItems = mongo_item_dao.findByLocation(tags, lat, lon)

    output = [item.toDict() for item in listOfItems]
    return jsonify(output), 200


@items_router.route('/api/items/search=<query>', methods=['GET'])
def get_all_items_sorted(query):
    # Get the tags if exists
    tags = ItemTags.get(request.args.get('tags'))

    # get list of all items using DAO and specifying the tags
    listOfItems = mongo_item_dao.findAll(tags)

    # if nothing in db, don't do any similarity comparisons
    if not listOfItems:
        return jsonify([]), 200

    queriedItem = Item(name=query, desc="")

    simMatch = ItemSimilarity(simModel)
    simMatch.addItems(listOfItems)
    simMatch.scoreItems(queriedItem)
    items = simMatch.getSortedItems(getScores=True)

    index = len(items)

    for i, (_, score) in enumerate(items):
        if score <= 0:
            index = i
            break

    items = items[0:index]

    if len(items) == 0:
        items = simMatch.getSortedItems()
        items = [(item, 0) for item in items if str(item).find(query) >= 0]

    output = [item[0].toDict() for item in items]

    return jsonify(output), 200

@items_router.route('/api/items/user=<query>', methods=['GET'])
def get_all_items_by_user(query):
    # Get the tags if provided
    tags = ItemTags.get(request.args.get('tags'))

    listOfItems = mongo_item_dao.findByMostRecent(tags, ' ')

    output = [item.toDict() for item in listOfItems if item.email == query]
    return jsonify(output), 200

    
@items_router.route('/api/sim_items', methods=['GET'])
def find_similar_items():
    """
        Route returns all item listings that are similar to the item listing
        created from the information recieved.

        Returns
        -------
        A list of item listing dictionaries (which are JSON compatible) and
        a code representing the success of the request.
    """

    # get all the information needed to make Item instance
    name = request.args.get('name')
    desc = request.args.get('desc')
    found = request.args.get('found') == 'true'
    location = ItemLocation([float(request.args.get('lat')), float(request.args.get('long'))])
    radius = float(request.args.get('radius'))
    tags = ItemTags.get(request.args.get('tags'))
    
    # TODO: This isn't even used at all here. If it is, it's going to have to be updated
    # Get the list of uploaded images and convert them to ItemImage objects
    uploadedImages = request.files.getlist('image')
    images = []
    """ for img in uploadedImages:
        encoded = standard_b64encode(img.read())
        encodedAsStr = encoded.decode()
        images.append(ItemImage(img.filename, img.mimetype, encodedAsStr)) """

    item = Item(name=name, desc=desc, found=found, location=location,
                radius=radius, tags=tags, images=images,
                timestamp=None, username=None, email=None)

    # want to check whenever an item is added if their are similar items to send notifications to
    listOfItems = mongo_item_dao.findAll(tags)
    if item.found is True:
        listOfItems = [item for item in listOfItems if item.found is False]
    else:
        listOfItems = [item for item in listOfItems if item.found is True]

    simMatch = ItemSimilarity(simModel)
    simMatch.addItems(listOfItems)

    simItems, foundStatus = getSimItems(item, simMatch)

    if len(simItems) > 3:
        simItems = simItems[0:3]

    return jsonify([x.toDict() for x in simItems]), 200

@items_router.route('/api/items', methods=['POST'])
def add_item():
    name = request.form['name']
    desc = request.form['desc']
    found = request.form['found'] == 'true'
    location = ItemLocation([float(request.form['latitude']),
                             float(request.form['longitude'])])
    radius = float(request.form['radius'])
    tags = ItemTags.get(request.form['tags'])

    timestamp = currTime()
    email = request.form['email']
    username = request.form['username']

    # Get the list of uploaded images and convert them to ItemImage objects
    uploadedImages = request.files.getlist('image')
    images = []
    for i, img in enumerate(uploadedImages):
        # file will be saved as './uploadedImages/<numImage>_<timestamp>_<origFileName&Type>
        filePath = str(i) + '_' + str(int(timestamp)) + '_' + img.filename
        img.save(IMAGE_FOLDER / filePath)
        images.append(ItemImage(img.filename, img.mimetype, filePath))
    
    item = Item(name=name, desc=desc, found=found, location=location,
                radius=radius, tags=tags, images=images,
                timestamp=timestamp, username=username, email=email)

    mongo_item_dao.insert(item)

    # want to check whenever an item is added if their are similar items to send notifications to
    listOfItems = mongo_item_dao.findAll(tags)
    if item.found is True:
        listOfItems = [item for item in listOfItems if item.found is False]
    else:
        listOfItems = [item for item in listOfItems if item.found is True]

    simMatch = ItemSimilarity(simModel)
    simMatch.addItems(listOfItems)

    simItems, foundStatus = getSimItems(item, simMatch)

    # send email to those who are notified
    if len(simItems) != 0:
        matching = [mongo_user_dao.findAllOptIn(simItem.email) for simItem in simItems]
        print("Users who have matching: " + str(matching))
        sendMail(item, simItems, foundStatus, matching)

    return jsonify(item.toDict()), 200


@items_router.route('/api/items/<Id>', methods=['PUT'])
def update_item(Id):
    # TODO: Update this to match the new architecture of objects
    # Actually let the user update items on the frontend

    name = request.form['name']
    desc = request.form['desc']
    found = request.form['found'] == 'true'
    location = ItemLocation([float(request.form['latitude']),
                             float(request.form['longitude'])])
    radius = float(request.form['radius'])
    tags = ItemTags.get(request.form['tags'])
    user = User(request.form['username'], request.form['email'], request.form['optIn'])

    item = Item(Id=Id, name=name, desc=desc, found=found, location=location,
                radius=radius, tags=tags, user=user)

    mongo_item_dao.update(item)
    return jsonify(item.toDict()), 200


@items_router.route('/api/items/<Id>', methods=['DELETE'])
def delete_item(Id):
    numDeleted = mongo_item_dao.remove(Id, request.args.get('email'))

    if numDeleted == 1:
        output = {'message': 'deleted'}
    else:
        output = {'message': 'not deleted'}

    return jsonify({'result': output}), 200


@items_router.route("/api/fetch_image/<filePath>")
def fetch_resource(filePath):
    print("THIS IS THE FILENAME "+ filePath)
    return send_from_directory(Path('../') / IMAGE_FOLDER, filePath)
