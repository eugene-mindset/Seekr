# Schedule Library imported 
from app.models.models import *
from app import mongo
import sched
import time 
import gensim.downloader as gens_api
from app.models.similarity import ItemSimilarity
from app.helpers import *
from math import radians, sin, cos, acos
from flask import Blueprint, jsonify, request, send_from_directory, send_file, Flask
from flask_mail import Mail, Message



embedding = gens_api.load('glove-wiki-gigaword-50')
items = mongo.db.items # our items collection in mongodb
mongo_item_dao = ItemDao(items) # initialize a DAO with the collection

app = Flask(__name__)

 def send_mail(queriedItem, items):
     app.config.update(dict(
         DEBUG = True,
         MAIL_SERVER = 'smtp.gmail.com',
         MAIL_PORT = 587,
         MAIL_USE_TLS = True,
         MAIL_USE_SSL = False,
         MAIL_USERNAME = 'seekr.oose@gmail.com',
         MAIL_PASSWORD = 'Seekroose!',
         MAIL_DEFAULT_SENDER = 'seekr.oose@gmail.com'
     ))

     mail = Mail(app)
     msg = Message("Similar Items Found",
                   recipients=[item.user.email])

     msg.html = "<b>These are some items that were added that may be similar to your lost item:<b>\n"

     for item in items:
         msg.html += item.name + "\n"
     mail.send(msg)

     return "done"


def distance(item1, item2):
    slat = radians(item1.location.coordinates[0])
    slon = radians(item1.location.coordinates[1])
    elat = radians(item2.location.coordinates[0])
    elon = radians(item2.location.coordinates[1])

    dist = 3958.8 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
    # dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
    return dist
# Functions setup 
      

def radius_cutoff(items, queriedItem):
    results = []

    for item in items:
        if distance(queriedItem, item) <= queriedItem.radius: #miles
            results.append(item)
    return results


def notify(queriedItem):
    
    listOfItems = mongo_item_dao.findAll(tags=0b0000_0000)
    
    # if queriedItem is a found item then only need to compare similarity with missing items and vice versa
    if queriedItem.found is True:
        listOfItems = [item for item in listOfItems if item.found is False]
    
    else:
         listOfItems = [item for item in listOfItems if item.found is True]
        
    listOfItems = radius_cutoff(listOfItems, queriedItem)
 
    if len(listOfItems) != 0:
        simMatch = ItemSimilarity(modelName=None)
        simMatch.model = embedding
        simMatch.addItems(listOfItems)
        simMatch.scoreItems(queriedItem)

        items = simMatch.getSortedItemsAndScores()
        similar_items = []

        for item, score in items:
            print("Score: " + str(score) + "...")
            if score >= 0.75:
                similar_items.append(item)
        if len(similar_items) != 0:
            send_mail(similar_items)
    else:
        print("NO ITEMS")


def notify_all():
    listOfItems = mongo_item_dao.findAll(tags)
    for item in listOfItems:
        notify(item)
        