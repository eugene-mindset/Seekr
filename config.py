class TestConfig(object):
    MONGO_DBNAME = "mydb"
    MONGO_URI = "mongodb://localhost:27017/" + MONGO_DBNAME

class ProdConfig(object):
    # MONGO_DBNAME = "mydb"
    MONGO_URI = "mongodb://user1:admin1@ds019028.mlab.com:19028/heroku_gvwmsj7z"


