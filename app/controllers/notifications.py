# Schedule Library imported 
from app.models.models import *
from app import mongo
import sched
import time 
import gensim.downloader as gens_api
from app.models.similarity import ItemSimilarity

from math import radians, sin, cos, acos

def distance(item1, item2):
    slat = radians(item1.location()[0])
    slon = radians(item1.location()[1])
    elat = radians(item2.location()[0])
    elon = radians(item2.location()[1])

    dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
    return dist

  
embedding = gens_api.load('glove-wiki-gigaword-50')
items = mongo.db.items # our items collection in mongodb
mongo_item_dao = ItemDao(items) # initialize a DAO with the collection
schedule = sched.scheduler(time.time, time.sleep)

# Functions setup 
      
def radius_cutoff(items, queriedItem):
    results = []

    for item in items:
        if distance(queriedItem, item) <= 5: #kilometers
            results.append(item)
    return results
    
def notify(queriedItem):
    listOfItems = mongo_item_dao.findAll(tags)
    listOfItems = radius_cutoff(listOfItems, queriedItem)
 
    simMatch = ItemSimilarity(modelName=None)
    simMatch.model = embedding
    simMatch.addItems(listOfItems)
    simMatch.scoreItems(queriedItem)

    items = [simMatch.getSortedItemsAndScores()]

    for (item, score) in items:
        if score >= 0.75:
            # email item.user.email

# Task scheduling 
# After every 10mins geeks() is called.  
#    schedule.every(5).seconds.do(geeks) 
  
# Loop so that the scheduling task 
# keeps on running all time. 
while True: 
  
    # Checks whether a scheduled task  
    # is pending to run or not 
    #schedule.run_pending() 
    #time.sleep(1) 
    schedule.enter(10, 1, geeks)
    schedule.run()