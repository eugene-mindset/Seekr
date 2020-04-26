from abc import abstractmethod
from enum import IntFlag

from bson.objectid import ObjectId

from app.mongo_inst import mongo


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

        # Register the location attribute for documents in mongo to be used as a
        # geospatial index for querying
        self.collection.create_index([('location', '2dsphere' )])

    def findById(self, Id):
        # Get the item from our mongodb collection
        itemDoc = self.collection.find_one({"_id": ObjectId(Id)})

        # Serialize it into an Item object
        newItem = Item.fromDict(itemDoc)

        return newItem

    def findAll(self, tags):
        # Mongo query to get the items that have the specified tags from our
        # mongodb collection
        filteredItems = self.collection.find({
            'tags': {
                '$bitsAllSet': int(tags)
            }
        })

        # Serialize documents into Item objects and return them in a list
        return [Item.fromDict(itemDoc) for itemDoc in filteredItems]

    def findByLocation(self, tags, lat, lon):
        # Mongo query to retrieve the items sorted by proximty to the
        # latitude and longitude and also have the specified tags
        filteredItems = self.collection.find({
            '$and': [
                {
                    "location": {
                        '$nearSphere': [float(lat), float(lon)]
                    }
                },
                {
                    'tags': {
                        '$bitsAllSet': int(tags)
                    }
                }
            ]
        })

        # Serialize documents into Item objects and return them in a list
        return [Item.fromDict(itemDoc) for itemDoc in filteredItems]

    def findByMostRecent(self, tags):
        # Mongo query to retrieve the items sorted by their timestamp in
        # descending order and also have the speicifed tags
        filteredItems = self.collection.find({
            'tags': {
                '$bitsAllSet': int(tags)
            }
        }).sort([('timestamp', -1)])

        # Serialize documents into Item objects and return them in a list
        return [Item.fromDict(itemDoc) for itemDoc in filteredItems]

    def findByQuery(self, query):
        queriedItems = self.collection.find(query)

        # Serialize documents into Item objects and return them in a list
        return [Item.fromDict(itemDoc) for itemDoc in queriedItems]

    def insert(self, item):
        data = item.toDict() # Get item info formatted in a JSON friendly manner
        data.pop('id') # Remove the id field

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
        #data.pop('imageName') # remove imageName, don't know how we would handle an update to an image???
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
                 radius=None, tags=None, images=[], timestamp=None,
                 user=None):
        self.Id = Id                # Should be a string
        self.name = name            # Should be a string
        self.desc = desc            # Should be a string
        self.found = found          # Should be a bool
        self.location = location    # Should be a ItemLocation object
        self.radius = radius        # Should be a float or int
        self.tags = tags            # Should be an ItemTags enum
        self.images = images        # Should be a list of ItemImage objects
        self.timestamp = timestamp  # Should be a float
        self.user = user            # Should be a User object

    @classmethod
    def fromDict(cls, doc):
        item = cls()
        item.Id = str(doc['_id'])
        item.name = doc['name']
        item.desc = doc['desc']
        item.found = doc['found']
        item.location = ItemLocation.fromDict(doc['location'])
        item.radius = doc['radius']
        item.tags = ItemTags(doc['tags'])
        item.images = [ItemImage.fromDict(img) for img in doc['images']]
        item.timestamp = doc['timestamp']
        item.user = User.fromDict(doc['user'])

        return item

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
    def images(self):
        return self.__images

    @images.setter
    def images(self, images):
        self.__images = images
    
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
        if self.images != otherItem.images:
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

    def toDict(self):
        output = {
            'id'        : self.Id,
            'name'      : self.name,
            'desc'      : self.desc,
            'found'     : self.found,
            'location'  : self.location.toDict() if self.location is not None else 'None',
            'radius'    : self.radius,
            'tags'      : ItemTags.toInt(self.tags),
            'images'    : [i.toDict() for i in self.images],
            'timestamp' : self.timestamp,
            'user'      : self.user.toDict() if self.user is not None else 'None'
        }

        return output

class UserDao(DatabaseObject):

    def __init__(self, collection):
        super().__init__(collection)

        # Register the location attribute for documents in mongo to be used as a
        # geospatial index for querying
        self.collection.create_index([('location', '2dsphere' )])

    def findById(self, Id):
        # Get the item from our mongodb collection
        UserDoc = self.collection.find_one({"_id": ObjectId(Id)})

        # Serialize it into an Item object
        newUser = User.fromDict(UserDoc)

        return newUser

    def findAll(self):
        # Mongo query to get the items that have the specified tags from our
        # mongodb collection
        filteredUsers = self.collection.find()

        # Serialize documents into Item objects and return them in a list
        return [User.fromDict(userDoc) for userDoc in filteredUsers]

    def insert(self, user):
        data = user.toDict() # Get item info formatted in a JSON friendly manner
        data.pop('id') # Remove the id field

        # Insert the item into our mongodb collection,
        # get the ID it was assigned, give the item that id
        user_id = self.collection.insert_one(data).inserted_id
        new_user = self.collection.find_one({'_id': user_id})
        user.Id = str(new_user['_id'])

        return user # TODO: The returned item is never used, remove this line at some point

    def update(self, user):
        Id = user.Id
        data = user.toDict() # Get item info formatted in a JSON friendly manner
        data.pop('id') # remove the id, shouldn't be updating it

        # find the item in our mongodb collection by its id,
        # update it with the new data
        self.collection.find_one_and_update({'_id': ObjectId(Id)}, {
            "$set": data
        }, upsert=False)

        return user # TODO: The returned item is never used, remove this line at some point

    def remove(self, Id):
        # Delete the item frmo our mongodb collection by its id
        returned = self.collection.delete_one({'_id': ObjectId(Id)})
        return returned.deleted_count


class User:

    def __init__(self, Id=None, name=None, email=None, optIn=None):
        self.Id = Id
        self.name = name    # Should be a string
        self.email = email  # Should be a string
        self.optIn = optIn  # Should be a boolean

    @classmethod
    def fromDict(cls, doc):
        user = cls()
        user.Id = str(doc['_id'])
        user.name = doc['name']
        user.email = doc['email']
        user.optIn = doc['optIn']

        return user

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
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def optIn(self):
        return self.__optIn
    
    @optIn.setter
    def optIn(self, optIn):
        self.__optIn = optIn

    def __eq__(self, otherUser):
        if self.Id != otherUser.Id:
            return False
        if self.name != otherUser.name:
            return False
        if self.email != otherUser.email:
            return False
        if self.optIn != otherUser.optIn:
            return False
        return True

    def __str__(self):
        return self.name + ': ' + self.email + ', ' + self.optIn

    def __repr__(self):
        return str(self)

    def toDict(self):
        output = {
            'id'    : self.Id,
            'name'  : self.name,
            'email' : self.email,
            'optIn' : self.optIn
        }

        return output


class ItemLocation:

    def __init__(self, coordinates=None):
        self.coordinates = coordinates  # Should be a list or tuple with two elements, both floats

    @classmethod
    def fromDict(cls, doc):
        location = cls()
        location.coordinates = doc['coordinates']

        return location

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


class ItemImage:

    def __init__(self, imageName=None, imageType=None, imageData=None):
        self.imageName = imageName  # Should be a string
        self.imageType = imageType  # Should be a string (image/png or image/jpeg)
        self.imageData = imageData  # Should be a string (standard base64)

    @classmethod
    def fromDict(cls, doc):
        image = cls()
        image.imageName = doc['imageName']
        image.imageType = doc['imageType']
        image.imageData = doc['imageData']

        return image

    @property
    def imageName(self):
        return self.__imageName

    @imageName.setter
    def imageName(self, imageName):
        self.__imageName = imageName

    @property
    def imageType(self):
        return self.__imageType

    @imageType.setter
    def imageType(self, imageType):
        self.__imageType = imageType

    @property
    def imageData(self):
        return self.__imageData

    @imageData.setter
    def imageData(self, imageData):
        self.__imageData = imageData

    def __eq__(self, otherItemImage):
        if self.imageName != otherItemImage.imageName:
            return False
        if self.imageType != otherItemImage.imageType:
            return False
        if self.imageData != otherItemImage.imageData:
            return False
        return True

    def __str__(self):
        return self.imageName

    def __rept__(self):
        return str(self)

    def toDict(self):
        output = {
            'imageName' : self.imageName,
            'imageType' : self.imageType,
            'imageData' : self.imageData
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
