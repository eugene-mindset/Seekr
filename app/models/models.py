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

    def findById(self, Id):
        item = self.collection.find_one({"_id": ObjectId(Id)})
        newItem = Item(str(item['_id']), item['name'], item['found'],
                       item['desc'], item['location'], item['tags'], item['imageName'])
        return newItem

    # DEPRECATED
    def findByName(self, name=None):
        listOfItems = []
        toSearch = self.collection.find({"name": name})
        for item in toSearch:
            newItem = Item(str(item.get('_id')), item.get('name'),
                           item.get('found'), item.get('desc'),
                           item.get('location'), item.get('imageName'))
            listOfItems.append(newItem)
            #Get timestamp of object created  
            print(item.get('_id').generation_time)

        return listOfItems

    def findAll(self, tags=None):
        listOfItems = []
        allItems = self.collection.find()
        
        for item in allItems:
            newItem = Item(str(item.get('_id')), item.get('name'),
                           item.get('found'), item.get('desc'),
                           item.get('location'), item.get('tags'), item.get('imageName'))
            if (len(tags) == 0): # no tags, add all
                listOfItems.append(newItem)
            else: # yes tags, filter
                containsAllTags = True
                for tag in tags:
                    if tag not in item.get('tags'):
                        containsAllTags = False
                if (containsAllTags): listOfItems.append(newItem)

        return listOfItems

    def insert(self, item):
        name = item.name
        found = item.found
        desc = item.desc
        location = item.location
        tags = item.tags
        imageName = item.imageName
        
        item_id = self.collection.insert_one({
            'name': name,
            'found': found,
            'desc': desc,
            'location': location,
            'tags': tags,
            'imageName': imageName
        }).inserted_id
        new_item = self.collection.find_one({'_id': item_id})
        item.Id = str(new_item['_id'])
        return item

    def update(self, item):
        Id = item.Id
        name = item.name
        found = item.found
        desc = item.desc
        location = item.location
        tags = item.tags
        self.collection.find_one_and_update({'_id': ObjectId(Id)}, {
            "$set": {
                "name": name,
                'found': found,
                'desc': desc,
                'location': location,
                'tags': tags
            }
        }, upsert=False)
        return item

    def remove(self, Id):
        returned = self.collection.delete_one({'_id': ObjectId(Id)})
        return returned.deleted_count


class Item:

    def __init__(self, Id=None, name=None, found=None, desc=None,
                 location=None, tags=None, imageName=None):
        self.Id = Id
        self.name = name
        self.found = found
        self.desc = desc
        self.location = location
        self.tags = tags
        self.imageName = imageName


    @property
    def Id(self):
        return self.__Id

    @Id.setter
    def Id(self, Id):
        self.__Id = Id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def found(self):
        return self.__found

    @found.setter
    def found(self, found):
        self.__found = found

    @property
    def desc(self):
        return self.__desc

    @desc.setter
    def desc(self, desc):
        self.__desc = desc

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, location):
        self.__location = location
        
    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, tags):
        self.__tags = tags

    def __eq__(self, otherItem):
        if self.Id != otherItem.Id:
            return False
        if self.name != otherItem.name:
            return False
        if self.found != otherItem.found:
            return False
        if self.desc != otherItem.desc:
            return False
        if self.location != otherItem.location:
            return False
        if set(self.tags) != set(otherItem.tags): # tags is a list of strings
            return False
        return True

    # magical formula to determine if a word is similar to another word
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

            return result

        return 1

    def toDict(self):
        output = {
            'id': self.Id,
            'name': self.name,
            'found': self.found,
            'desc': self.desc,
            'location': self.location,
            'tags' : self.tags,
            'imageName': self.imageName
        }
        return output
