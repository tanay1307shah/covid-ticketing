import pymongo


def setupDB(db, collection):
    uri = "mongodb://covid123:covid123@ds034807.mlab.com:34807/covid-ticketing-db?retryWrites=false"
    client = pymongo.MongoClient(uri)
    db = client[db]  # identifying the db
    return db
