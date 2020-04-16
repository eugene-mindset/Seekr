from app import mongo
from abc import abstractmethod
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
        # Get the item from our mongodb collection
        item = self.collection.find_one({"_id": ObjectId(Id)})
        # Serialize it into an Item object
        newLocation = Location(item['location']['coordinates'])
        newUser = User(name=item['user']['name'], email=item['user']['email'],
                       phone=item['user']['phone'])
        newItem = Item(str(item['_id']), item['name'], item['desc'],
                       item['found'], newLocation, item['radius'],
                       ItemTags(item['tags']), item['imageName'],
                       item['timestamp'], newUser, item['distance'])

        return newItem

    def findAll(self, tags):
        # Get all the items from our mongodb collection
        listOfItems = []
        allItems = self.collection.find()

        for item in allItems:
            # Serialize it into an Item object
            newLocation = Location(item['location']['coordinates'])
            newUser = User(name=item['user']['name'], email=item['user']['email'],
                           phone=item['user']['phone'])
            newItem = Item(str(item['_id']), item['name'], item['desc'],
                           item['found'], newLocation, item['radius'],
                           ItemTags(item['tags']), item['imageName'],
                           item['timestamp'], newUser, item['distance'])

            # check if we're not searching with tags
            # or if item has all the tags being searched for
            if (tags == ItemTags.NONE) or (tags & newItem.tags == tags):
                listOfItems.append(newItem)

        return listOfItems

    def insert(self, item):
        data = item.toDict() # Get item info formatted in a JSON friendly manner
        data.pop('id') # Remove the id

        # Insert the item into our mongodb collection,
        # get the ID it was assigned, give the item that id
        item_id = self.collection.insert_one(data).inserted_id
        new_item = self.collection.find_one({'_id': item_id})
        item.Id = str(new_item['_id'])

        return item # TODO: The returned item is never used, remove this line at some point

    def update(self, item):
        Id = item.Id
        data = item.toDict() # Get item info formatted in a JSON friendly manner
        data.pop('id') # remove the id, shouldn't be updating it
        data.pop('timestamp') # remove the timestamp, shouldn't be updating it
        data.pop('imageName') # remove imageName, don't know how we would handle an update to an image???
        # TODO: handle image updates

        # find the item in our mongodb collection by its id,
        # update it with the new data
        self.collection.find_one_and_update({'_id': ObjectId(Id)}, {
            "$set": data
        }, upsert=False)

        return item # TODO: The returned item is never used, remove this line at some point

    def remove(self, Id):
        # Delete the item frmo our mongodb collection by its id
        returned = self.collection.delete_one({'_id': ObjectId(Id)})
        return returned.deleted_count


class Item:

    def __init__(self, Id=None, name=None, desc=None, found=None, location=None,
                 radius=None, tags=None, imageName=None, timestamp=None,
                 user=None, distance=None):
        self.Id = Id                # Should be a string
        self.name = name            # Should be a string
        self.desc = desc            # Should be a string
        self.found = found          # Should be a bool
        self.location = location    # Should be a Location object
        self.radius = radius        # Should be a float or int
        self.tags = tags            # Should be an ItemTags enum
        self.imageName = imageName  # Should be a string
        self.timestamp = timestamp  # Should be a float
        self.user = user            # Should be a User object
        self.distance = distance    # Should be a float

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
    def desc(self):
        return self.__desc

    @desc.setter
    def desc(self, desc):
        self.__desc = desc

    @property
    def found(self):
        return self.__found

    @found.setter
    def found(self, found):
        self.__found = found

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, location):
        self.__location = location

    @property
    def radius(self):
        return self.__radius
    
    @radius.setter
    def radius(self, radius):
        self.__radius = radius
        
    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, tags):
        self.__tags = tags

    @property
    def imageName(self):
        return self.__imageName

    @imageName.setter
    def imageName(self, imageName):
        self.__imageName = imageName
    
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

    @property
    def distance(self):
        return self.__distance
    
    @distance.setter
    def distance(self, distance):
        self.__distance = distance

    def __eq__(self, otherItem):
        if self.Id != otherItem.Id:
            return False
        if self.name != otherItem.name:
            return False
        if self.desc != otherItem.desc:
            return False
        if self.found != otherItem.found:
            return False
        if self.location != otherItem.location:
            return False
        if self.radius != otherItem.radius:
            return False
        if self.tags != otherItem.tags:
            return False
        if self.imageName != otherItem.imageName:
            return False
        if self.timestamp != otherItem.timestamp:
            return False
        if self.user != otherItem.user:
            return False
        if self.distance != otherItem.distance:
            return False
        return True

    def __str__(self):
        return self.name + ': ' + self.desc

    def __repr__(self):
        return str(self)

    # TODO: delete this, no longer used because we have a better search algo now
    # magical formula to determine if a word is similar to another word
    # def compareItem(self, otherItem: 'Item', comparator=None):
    #     if comparator is None:
    #         total = []
    #         unique = set()

    #         if type(self.name) == str and type(self.desc) == str:
    #             tokensName = set(self.name.lower().split())
    #             tokensDesc = set(self.desc.lower().split())

    #             total += list(tokensName.union(tokensDesc))

    #         if type(otherItem.name) == str and type(otherItem.desc) == str:
    #             tokensName = set(otherItem.name.lower().split())
    #             tokensDesc = set(otherItem.desc.lower().split())

    #             total += list(tokensName.union(tokensDesc))

    #         unique = set(total)
    #         matches = len(total) - len(unique)
    #         result = matches

    #         return result

    #     return 1

    def toDict(self):
        output = {
            'id'        : self.Id,
            'name'      : self.name,
            'desc'      : self.desc,
            'found'     : self.found,
            'location'  : self.location.toDict() if self.location is not None else 'None',
            'radius'    : self.radius,
            'tags'      : ItemTags.toInt(self.tags),
            'imageName' : self.imageName,
            'timestamp' : self.timestamp,
            'user'      : self.user.toDict() if self.user is not None else 'None',
            'distance'  : self.distance
        }

        return output


class User:

    def __init__(self, name=None, email=None, phone=None):
        self.name = name    # Should be a string
        self.email = email  # Should be a string
        self.phone = phone  # Should be a string

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
            'name'  : self.name,
            'email' : self.email,
            'phone' : self.phone
        }

        return output


class Location:

    def __init__(self, coordinates=None):
        self.coordinates = coordinates # Should be a list or tuple with two elements, both floats

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
            'type'        : 'Point',
            'coordinates' : self.coordinates
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
