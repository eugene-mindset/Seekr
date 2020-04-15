# Schedule Library imported 
from app.models.models import *
from app import mongo
import sched
import time 
import gensim.downloader as gens_api
from app.models.similarity import ItemSimilarity

from math import radians, sin, cos, acos

embedding = gens_api.load('glove-wiki-gigaword-50')
items = mongo.db.items # our items collection in mongodb
mongo_item_dao = ItemDao(items) # initialize a DAO with the collection
schedule = sched.scheduler(time.time, time.sleep)

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

        for item, score in items:
            print("Score: " + str(score) + "...")
            if score >= 0.75:
                # email item.user.email
                print("The item name is: " + str(item.name) + " Score: " + str(score) + ".")
    else:
        print("NO ITEMS")


def notify_all():
    listOfItems = mongo_item_dao.findAll(tags)
    for item in listOfItems:
        notify(item)
        

# Task scheduling 
# After every 10mins geeks() is called.  
#    schedule.every(5).seconds.do(geeks) 
  
# Loop so that the scheduling task 
# keeps on running all time. 
def notify_by_time(queriedItem):
    while True: 
    # Checks whether a scheduled task  
    # is pending to run or not 
    #schedule.run_pending() 
    #time.sleep(1) 
        schedule.enter(60, 1, notify_all)
        schedule.run()