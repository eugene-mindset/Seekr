from abc import ABC, abstractmethod
from enum import IntFlag
from pathlib import Path

from bson.objectid import ObjectId

from app.mongo_inst import mongo

# Location of where images for items are stored
IMAGE_FOLDER = Path('./uploadedImages/')


class DaoFactory():
    """Factory for generating DAOs
    """
    def getDao(self, obj, args):
        """Instantiate a type of DAO and return it

        Arguments:
            obj {str} -- String denoting the DAO requested
            args {collection} -- the collection needed for the DAO to instantiate

        Returns:
            DatabaseObject -- gives the requested DAO type
        """
        if obj == 'item':
            return ItemDao(args)
        elif obj == 'user':
            return UserDao(args)
        else:
            return None


class DatabaseObject(ABC):
    """
        Interface that defines important methods for DAOs to implement. Cannot
        be instantiated.
    """

    def __init__(self, collection):
        self.collection = collection

    @abstractmethod
    def findById(self):
        """
            Get an object by id from self.collection.
        """

        pass

    @abstractmethod
    def insert(self):
        """
            Add an object to self.collection.
        """
        pass

    @abstractmethod
    def update(self):
        """
            Update object in self.collection.
        """
        pass

    @abstractmethod
    def remove(self):
        """
            Remove object from self.collection.
        """
        pass


class ItemDao(DatabaseObject):
    """
        Class acts as a DAO to convert MongoDB results to their abstract
        representation.
    """

    def __init__(self, collection):
        """
            Initialize ItemDao instance.

            Args:
                collection: the mongo DB to access
        """

        super().__init__(collection)

        # Register the location attribute for documents in mongo to be used as a
        # geospatial index for querying
        self.collection.create_index([('location', '2dsphere' )])
        # Register the name and description attributes for documents in mongo to
        # be used as a text index for searching
        self.collection.create_index([('name', 'text'), ('desc', 'text')])

    def findById(self, Id):
        """
            Get an item listing in self.collection by id.

            Args:
                Id: the corresponding id of the item listing to retrieve

            Returns:
                Item instance
        """
        # Get the item from our mongodb collection
        itemDoc = self.collection.find_one({"_id": ObjectId(Id)})

        # Serialize it into an Item object
        newItem = Item.fromDict(itemDoc)

        return newItem

    def findAll(self, tags):
        """
            Get all listings in self.collection that have the corresponding
            tags.

            Args:
                tags: the tags that every Item will have for it to be returned

            Returns:
                A list of Item instances
        """

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
        """
            Get all listings sorted by proximity to a location.

            Args:
                tags: the tags that every Item will have for it to be returned

            Returns:
                A list of Item instances
        """
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

    def findByMostRecent(self, tags, query):
        """
            Get all listings sorted by recency in creation.

            Args:
                tags: the tags that every Item will have for it to be returned
                query: words in query must appear in returned results

            Returns:
                A list of Item instances
        """

        # Mongo query to retrieve the items sorted by their timestamp in
        # descending order and also have the speicifed tags
        if (query.isspace()):
             filteredItems = self.collection.find({
                'tags': {
                    '$bitsAllSet': int(tags)
                }
            }).sort([('timestamp', -1)])
        else:
            filteredItems = self.collection.find({
                '$and': [
                    {
                        "$text": {
                            '$search': query,
                            '$language': 'english'
                        }
                    },
                    {
                        'tags': {
                            '$bitsAllSet': int(tags)
                        }
                    }
                ]
            }).sort([('timestamp', -1)])

        # Serialize documents into Item objects and return them in a list
        return [Item.fromDict(itemDoc) for itemDoc in filteredItems]

    def findByQuery(self, query):
        """
            Get all listings that match the query.

            Args:
                query: words in query must appear in returned results

            Returns:
                A list of Item instances
        """

        queriedItems = self.collection.find(query)

        # Serialize documents into Item objects and return them in a list
        return [Item.fromDict(itemDoc) for itemDoc in queriedItems]

    def insert(self, item):
        """
            Add an Item to self.collection.

            Args:
                item: the Item to be added

        """

        data = item.toDict() # Get item info formatted in a JSON friendly manner
        data.pop('id') # Remove the id field

        # Insert the item into our mongodb collection,
        # get the ID it was assigned, give the item that id
        item_id = self.collection.insert_one(data).inserted_id
        new_item = self.collection.find_one({'_id': item_id})
        item.Id = str(new_item['_id'])

    def update(self, item):
        """
            Update Item in self.collection.

            Args:
                item: the Item to be updated
        """

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

    def remove(self, Id, user):
        """
            Remove an Item from self.collection by its id.

            Args:
                Id: the id of the listing to remove
                user: the user that is trying to remove the item

            Returns:
                0 if unsuccesful in deletion, otherwise 1
        """


        # Delete the item from our mongodb collection by its id if it matches the sender's email
        toDelete = self.findById(Id)

        if user.canDelete(toDelete):
                # delete associated images
            for img in toDelete.images:
                pathToFile = IMAGE_FOLDER / img.imageData
                pathToFile.unlink()
            returned = self.collection.delete_one({'_id': ObjectId(Id)})
            return returned.deleted_count

        return 0


class Item:
    """
        Represents the items in the database.
    """

    def __init__(self, Id=None, name=None, desc=None, found=None, location=None,
        radius=None, tags=None, images=[], timestamp=None, username=None,
        email=None):
        """
            Initialize Item instance.

            Args:
                Id: the assigned id of self
                name: name of self
                desc: description of self
                found: If true, this indicates that self is a found item
                location: an ItemLocation instance representing the location of
                    self in long/lat
                radius: how far the search range of the listing should be
                tags: an ItemTags instance representing the tags of self
                images: the ItemImages belonging to self
                timestamp: the time self was made
                username: the username of the creator of self
                email: the email associated with self

        """

        self.Id = Id                # Should be a string
        self.name = name            # Should be a string
        self.desc = desc            # Should be a string
        self.found = found          # Should be a bool
        self.location = location    # Should be a ItemLocation object
        self.radius = radius        # Should be a float or int
        self.tags = tags            # Should be an ItemTags enum
        self.images = images        # Should be a list of ItemImage objects
        self.timestamp = timestamp  # Should be a float
        self.username = username    # Should be a string
        self.email = email          # Should be a string

    @classmethod
    def fromDict(cls, doc):
        """
            Take a dictionary and convert it into an Item

            Args:
                doc: the dictionary to convert

            Returns:
                the Item instance
        """
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
        item.username = doc['username']
        item.email = doc['email']

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
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, username):
        self.__username = username
        
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, email):
        self.__email = email

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
        if self.username != otherItem.username:
            return False
        if self.email != otherItem.email:
            return False
        return True

    def __str__(self):
        return self.name + ': ' + self.desc

    def __repr__(self):
        return str(self)

    def toDict(self):
        """
            Get dictionary representation of Item

            Returns:
                a dictionary
        """
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
            'username'  : self.username,
            'email'     : self.email if self.email is not None else 'None'
        }

        return output

# <<Interface>> AbstractUser
#      ^          ^
#     User       Admin

class UserDao(DatabaseObject):
    """
        DAO converts user information from results given from MongoDB queries to
        their corresponding class representation.
    """

    def __init__(self, collection):
        """
            Initialize DAO

            Args:
                collection: the DB to access
        """
        super().__init__(collection)

        # Register the location attribute for documents in mongo to be used as a
        # geospatial index for querying
        self.collection.create_index([('location', '2dsphere' )])

    def findById(self, Id):
        """
            Find user by Id in self.collection

            Args:
                Id: the id of the user to find

            Retuns:
                an AbstractUser instance
        """

        # Get the item from our mongodb collection
        userDoc = self.collection.find_one({"_id": ObjectId(Id)})

        # Serialize it into an User object
        newUser = User.fromDict(UserDoc)
        
        if (userDoc['isAdmin']):
            return Admin.fromDict(userDoc)
        else:
            return User.fromDict(userDoc)
        # return [User.fromDict(userDoc) for userDoc in filteredUsers]

    def findAllMatchingEmail(self, email):
        """
            Get all users with matching emails in self.collection.

            Args:
                email: the email to filter by

            Returns:
                list of AbstractUser instances
        """

        filteredUsers = self.collection.find({
            'email' : email
        })
        
        output = []
        # Serialize documents into Item objects and return them in a list
        for userDoc in filteredUsers:
            if (userDoc['isAdmin']):
                output.append(Admin.fromDict(userDoc))
            else:
                output.append(User.fromDict(userDoc))
        return output
    
    
        
    def findAllOptIn(self, email):
        """
            Get all users with matching emails in self.collection that opt-in
            to email notifications.

            Args:
                email: the email to filter by

            Returns:
                a list of User instances
        """

        filteredUsers = self.collection.find({
            'email' : email,
            'optIn' : "true"
        })
        
        for userDoc in filteredUsers:
            return User.fromDict(userDoc).email

    def findAll(self):
        """
            Get all users in self.collection.

            Returns:
                a list of AbstractUsers
        """

        # Mongo query to get the items that have the specified tags from our
        # mongodb collection
        filteredUsers = self.collection.find()

        output = []
        # Serialize documents into Item objects and return them in a list
        for userDoc in filteredUsers:
            if (userDoc['isAdmin']):
                output.append(Admin.fromDict(userDoc))
            else:
                output.append(User.fromDict(userDoc))
        return output
    
    
    def insert(self, user):
        """
            Add an User to self.collection

            Args:
                user: the user that is being inserted
        """
        data = user.toDict() # Get item info formatted in a JSON friendly manner
        data.pop('id') # Remove the id field

        # Insert the user into our mongodb collection,
        # get the ID it was assigned, give the user that id
        user_id = self.collection.insert_one(data).inserted_id
        new_user = self.collection.find_one({'_id': user_id})
        user.Id = str(new_user['_id'])

    def update(self, user):
        """
            Update a users information in self.collection.

            Args:
                user: the user that is being updated
        """

        Id = user.Id
        data = user.toDict() # Get item info formatted in a JSON friendly manner
        data.pop('id') # remove the id, shouldn't be updating it

        # find the item in our mongodb collection by its id,
        # update it with the new data
        self.collection.find_one_and_update({'_id': ObjectId(Id)}, {
            "$set": data
        }, upsert=False)


    def remove(self, Id):
        """
            Remove a User from self.collection by its id.

            Args:
                Id: the id of the listing to remove

            Returns:
                The number of users deleted
        """

        # Delete the item frmo our mongodb collection by its id
        returned = self.collection.delete_one({'_id': ObjectId(Id)})
        return returned.deleted_count

class AbstractUser(ABC):
    def __init__(self, Id=None, name=None, email=None, optIn=None, listOfItemIds=None):
        self.Id = Id
        self.name = name                # Should be a string
        self.email = email              # Should be a string
        self.optIn = optIn              # Should be a boolean
        self.listOfItemIds = listOfItemIds  # Should be a list of strings
        
    @classmethod
    def fromDict(cls, doc):
        abstractUser = cls()
        abstractUser.Id = str(doc['_id'])
        abstractUser.name = doc['name']
        abstractUser.email = doc['email']
        abstractUser.optIn = doc['optIn']
        abstractUser.listOfItemIds = doc['listOfItemIds']
        return abstractUser 

    @abstractmethod
    def toDict(self):
        # current instance (self) and converts to dictionary
        pass
    
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
    
    @property
    def listOfItemIds(self):
        return self.__listOfItemIds
    
    @listOfItemIds.setter
    def listOfItemIds(self, listOfItemIds):
        self.__listOfItemIds = listOfItemIds
    
    def addItem(self, itemId):
        self.__listOfItemIds.append(itemId)
    
    def __eq__(self, otherUser):
        if self.Id != otherUser.Id:
            return False
        if self.name != otherUser.name:
            return False
        if self.email != otherUser.email:
            return False
        if self.optIn != otherUser.optIn:
            return False
        if self.listOfItemIds != otherUser.listOfItemIds:
            return False
        return True
    
    def __str__(self):
        return self.name + ': ' + self.email + ', ' + self.optIn + ', ' + self.listOfItemIds

    def __repr__(self):
        return str(self)
    
    @abstractmethod
    def canDelete(self, item):
        pass
        
    
class User(AbstractUser):

    def __init__(self, Id=None, name=None, email=None, optIn=None, listOfItemIds=None):
        super().__init__(Id, name, email, optIn, listOfItemIds)

    @classmethod
    def fromDict(cls, doc):
        user = cls()
        user.Id = str(doc['_id'])
        user.name = doc['name']
        user.email = doc['email']
        user.optIn = doc['optIn']
        user.listOfItemIds = doc['listOfItemIds']

        return user 
    
    # when convert to dict, set isAdmin to false
    def toDict(self):
        output = {
            'id'            : self.Id,
            'name'          : self.name,
            'email'         : self.email,
            'optIn'         : self.optIn,
            'isAdmin'       : False,
            'listOfItemIds' : self.listOfItemIds
        }
        return output
    
    def canDelete(self, item):
        return item.Id in self.listOfItemIds
        # return self.email == item.email


class Admin(AbstractUser):
    def __init__(self, Id=None, name=None, email=None, optIn=None, listOfItemIds=None):
        super().__init__(Id, name, email, optIn, listOfItemIds)

    @classmethod
    def fromDict(cls, doc):
        admin = cls()
        admin.Id = str(doc['_id'])
        admin.name = doc['name']
        admin.email = doc['email']
        admin.optIn = doc['optIn']
        admin.listOfItemIds = doc['listOfItemIds']

        return admin 

    # when convert to dict, set isAdmin to true
    def toDict(self):
        output = {
            'id'            : self.Id,
            'name'          : self.name,
            'email'         : self.email,
            'optIn'         : self.optIn,
            'isAdmin'       : True,
            'listOfItemIds' : self.listOfItemIds

        }
        return output
    
    # Admin can always delete other people's items
    def canDelete(self, item):
        return True
    
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
        self.imageData = imageData  # Should be a string (path to file)

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
