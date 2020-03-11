from app import mongo
from abc import ABCMeta, abstractmethod
from bson.objectid import ObjectId
from flask import jsonify

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
        newItem = Item(str(item['_id']), item['name'], item['found'], item['desc'])
        return newItem

    def findByName(self, name=None):
        listOfItems = []
        toSearch = self.collection.find() if name == None else self.collection.find({"name" : name})
        for item in toSearch:
            newItem = Item(str(item.get('_id')), item.get('name'), item.get('found'), item.get('desc'))
            listOfItems.append(newItem)
            
        return listOfItems

    def insert(self, item):
        name = item.getName()
        found = item.getFound()
        desc = item.getDesc()
        item_id = self.collection.insert({'name' : name, 'found': found, 'desc':desc})
        new_item = self.collection.find_one({'_id' : item_id})
        item.setId(str(new_item['_id']))
        return item

    def update(self, item):
        id = item.getId()
        name = item.getName()
        found = item.getFound()
        desc = item.getDesc()
        self.collection.find_one_and_update({'_id':ObjectId(id)}, {"$set": {"name": name, 'found': found, 'desc': desc}}, upsert=False)
        return item

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

    def __eq__(self, otherItem):
        if self.id != otherItem.id:
            return False
        if self.name != otherItem.name:
            return False
        if self.found != otherItem.found:
            return False
        if self.desc != otherItem.desc:
            return False
        return True

    def compareItem(self, otherItem: 'Item', comparator=None):
        if comparator is None:
            total = []
            unique = set()

            if type(self.name) == str and type(self.desc) == str:
                tokensName = set(self.name.lower().split())
                tokensDesc = set(self.desc.lower().split())

                total += list(tokensName.union(tokensDesc))

            if type(otherItem.name) == str and type(otherItem.desc) == str:
                tokensName = set(otherItem.name.lower().split())
                tokensDesc = set(otherItem.desc.lower().split())

                total += list(tokensName.union(tokensDesc))
            
            unique = set(total)
            matches = len(total) - len(unique)
            result = matches

            # print(otherItem.name + ":", otherItem.desc, result, total, unique)

            return result

        return 1
    
    def toDict(self):
        output = {'id': self.id, 'name' : self.name, 'found': self.found, 'desc': self.desc}