from app import mongo
from abc import ABCMeta, abstractmethod
from bson.objectid import ObjectId
from flask import jsonify
from enum import IntFlag

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
                    item['desc'], item['location'], ItemTags(item['tags']), item['imageName'], item['radius'], item['timestamp'], item['user'])
        return newItem

    # DEPRECATED
    def findByName(self, name=None):
        listOfItems = []
        toSearch = self.collection.find({"name": name})
        for item in toSearch:
            newItem = Item(str(item.get('_id')), item.get('name'),
                            item.get('found'), item.get('desc'),
                            item.get('location'), item.get('imageName'), item.get('radius'), item.get('timestamp'), item.get('user'))
            listOfItems.append(newItem)
            #Get timestamp of object created

        return listOfItems

    def findAll(self, tags):
        listOfItems = []
        allItems = self.collection.find()

        for item in allItems:
            newItem = Item(str(item.get('_id')), item.get('name'),
                        item.get('found'), item.get('desc'),
                        item.get('location'), ItemTags.get(item.get('tags')), item.get('imageName'), item.get('radius'), item.get('timestamp'),
                        item.get('user'))

            if (tags == ItemTags.NONE) or (tags & newItem.tags == tags): # no tags, add all
                listOfItems.append(newItem)


        return listOfItems

    def insert(self, item):
        name = item.name
        found = item.found
        desc = item.desc
        location = item.location
        tags = ItemTags.toInt(item.tags)
        imageName = item.imageName
        radius = item.radius
        timestamp = item.timestamp
        user = item.user
        item_id = self.collection.insert_one({
            'name': name,
            'found': found,
            'desc': desc,
            'location': location,
            'tags': tags,
            'imageName': imageName,
            'radius': radius,
            'timestamp': timestamp,
            'user': user
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
        tags = ItemTags.toInt(item.tags)
        radius = item.radius
        timestamp = item.timestamp
        user = item.user
        self.collection.find_one_and_update({'_id': ObjectId(Id)}, {
            "$set": {
                "name": name,
                'found': found,
                'desc': desc,
                'location': location,
                'tags': tags,
                'radius': radius,
                'timestamp': timestamp,
                'user': user
            }
        }, upsert=False)
        return item

    def remove(self, Id):
        returned = self.collection.delete_one({'_id': ObjectId(Id)})
        return returned.deleted_count


class Item:

    def __init__(self, Id=None, name=None, found=None, desc=None,
                location=None, tags=None, imageName=None, radius=None, timestamp=None, user=None):
        self.Id = Id
        self.name = name
        self.found = found
        self.desc = desc
        self.location = location
        self.tags = tags
        self.imageName = imageName
        self.radius = radius
        self.timestamp = timestamp
        self.user = user

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

    @property
    def radius(self):
        return self.__radius
    
    @radius.setter
    def radius(self, radius):
        self.__radius = radius
    
    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self.__timestamp = timestamp

    @property
    def user(self):
        return self.__user
    
    @user.setter
    def user(self, user):
        self.__user = user

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
        if self.radius != otherItem.radius:
            return False
        if self.timestamp != otherItem.timestamp:
            return False
        if self.user != otherItem.user:
            return False
        return True

    def __str__(self):
        return self.name + ': ' + self.desc

    def __repr__(self):
        return str(self)

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
            'tags' : ItemTags.toInt(self.tags),
            'imageName': self.imageName,
            'radius' : self.radius,
            'timestamp' : self.timestamp,
            'user': self.user
        }

        return output

class User:

    def __init__(self, name=None, email=None, phone=None):
        self.name = name
        self.email = email
        self.phone = phone

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        self.__phone = phone

    def __eq__(self, otherUser):
        if self.name != otherUser.name:
            return False
        if self.email != otherUser.email:
            return False
        if self.phone != otherUser.phone:
            return False
        return True

    def __str__(self):
        return self.name + ': ' + self.email + ', ' + self.phone

    def __repr__(self):
        return str(self)

    def toDict(self):
        output = {
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }

        return output

class Location:

    def __init__(self, coordinates=None):
        self.coordinate = coordinates

    @property
    def coordinates(self):
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        self.__coordinates = coordinates

    def __eq__(self, otherLoc):
        if self.coordinates != otherLoc.coordinates:
            return False
        return True

    def __str__(self):
        return 'Point at: ' + self.coordinates

    def __repr__(self):
        return str(self)

    def toDict(self):
        output = {
            'type': 'Point',
            'coordinates': self.coordinates
        }

        return output

class ItemTags(IntFlag):
    NONE        = 0b0000_0000
    TECH        = 0b0000_0001
    CLOTHING    = 0b0000_0010
    JEWELRY     = 0b0000_0100
    PET         = 0b0000_1000
    PERSONAL    = 0b0001_0000
    APPAREL     = 0b0010_0000
    OTHER       = 0b0100_0000

    @staticmethod
    def get(x):
        val = ItemTags.NONE
        try:
            val = ItemTags(int(x))
            return val
        except ValueError:
            return ItemTags.NONE
        except TypeError:
            return ItemTags.NONE

    @staticmethod
    def toInt(x):
        val = ItemTags.NONE
        try:
            val = ItemTags(int(x))
            return int(val)
        except ValueError:
            return 0
        except TypeError:
            return ItemTags.NONE
