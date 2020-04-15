# Schedule Library imported 
from app.models.models import *
from app import mongo
import sched
import time 
import gensim.downloader as gens_api
from app.models.similarity import ItemSimilarity

  
embedding = gens_api.load('glove-wiki-gigaword-50')
items = mongo.db.items # our items collection in mongodb
mongo_item_dao = ItemDao(items) # initialize a DAO with the collection
schedule = sched.scheduler(time.time, time.sleep)

# Functions setup 
      
def notify(queriedItem):
    listOfItems = mongo_item_dao.findAll(tags)
 
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