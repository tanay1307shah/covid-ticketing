from flask import Flask, request, Response, render_template, jsonify
import json
import pymongo
from bson.json_util import dumps
from flask_swagger import swagger

app = Flask(__name__, template_folder='./client') 
  
@app.route("/")
def homePage():
    return render_template('index.html')

@app.route("/test")
def hello():
    return "Hello World!"


def setupDB(db, collection):
    uri = "mongodb://binoy123:binoy123@ds155634.mlab.com:55634/apifortest?retryWrites=false"
    client = pymongo.MongoClient(uri)
    db = client[db]  # identifying the db
    collection = db[collection]  # identifying the collection/table
    return collection



