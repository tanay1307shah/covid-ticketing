import pymongo
def setupDB(db, collection):
    uri = "mongodb://binoys123:binoys123@ds034807.mlab.com:34807/covid-ticketing-db"
    client = pymongo.MongoClient(uri)
    db = client[db]  # identifying the db
    collection = db[collection]  # identifying the collection/table
    return collection