class TestConfig(object):
    MONGO_DBNAME = "testdb"
    MONGO_URI = "mongodb://localhost:27017/" + MONGO_DBNAME


class ProdConfig(object):
    MONGO_DBNAME = "proddb"
    MONGO_URI = "mongodb://localhost:27017/" + MONGO_DBNAME
