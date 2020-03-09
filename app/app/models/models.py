from app import mongo
from abc import ABCMeta, abstractmethod
from bson.objectid import ObjectId

class DatabaseObject:
    def __init__(self, collection):
        self.collection = collection
    @abstractmethod
    def findById(self):
        raise NotImplementedError
    @abstractmethod
    def insert(self):
        raise NotImplementedError
    @abstractmethod
    def update(self):
        raise NotImplementedError
    @abstractmethod
    def remove(self):
        raise NotImplementedError

class ItemDao(DatabaseObject):

    def __init__(self, collection):
        super().__init__(collection)

    def findById(self, id):
        item = self.collection.find_one({"_id" : ObjectId(id)})
        return item

    def findByName(self, name=None):
        output = []
        toSearch = self.collection.find() if name == None else self.collection.find({"name" : name})
        for item in toSearch:
            output.append({'id': str(item['_id']), 'name' : item['name'], 'found': item['found'], 'desc': item['desc']}) 
        return output

    def insert(self, name, found, desc):
        item_id = self.collection.insert({'name' : name, 'found': found, 'desc':desc})
        new_item = self.collection.find_one({'_id' : item_id})
        output = {'id': str(new_item['_id']), 'name' : new_item['name'], 'found': found, 'desc': new_item['desc']}
        return output

    def update(self, id, name, found, desc):
        self.collection.find_one_and_update({'_id':ObjectId(id)}, {"$set": {"name": name, 'found': found, 'desc': desc}}, upsert=False)
        item = self.collection.find_one({'_id' : ObjectId(id)})
        output = {'id': str(item['_id']), 'name' : item['name'], 'found': found, 'desc': item['desc']}
        return output

    def remove(self, id):
        returned = self.collection.delete_one({'_id': ObjectId(id)})
        return returned.deleted_count
    
class Item:
    #TODO remove placeholder when location can be added
    def __init__(self, id=None, name=None, found=None, desc=None, location=None):
        self.id = id
        self.name = name
        self.found = found
        self.desc = desc
        self.location = location

    def getId(self):
        return self.id

    def setId(self, id):
        self.id = id

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name
        
    def getFound(self):
        return self.found

    def setFound(self, found):
        self.found = found

    def getDesc(self):
        return self.desc

    def setDesc(self, desc):
        self.desc = desc

    def getLocation(self):
        return self.location

    def setLocation(self, location):
        self.location = location

    def compareItems(self, otherItem):
        #TODO implement comparator
        return True