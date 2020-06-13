from flask import Flask, request, Response, render_template
import pymongo
import json
from bson.json_util import dumps
app = Flask(
    __name__, template_folder='./client')
table = None


@app.route("/test")
def hello():
    return "Hello World!"

@app.route("/")
def homePage():
    return render_template('home.html')    

#------------REST API Code----------------------
@app.route("/products", methods=['GET', 'POST', 'DELETE'])
def products():
    global table
    if table is None:
        table = setupDB("apifortest", "products")

    # This section checks if the incoming request is GET and 'View all' content into mlab db
    if request.method == "GET":
        try:
            cursor = table.find()   # operation on table to get all data
            response = list()
            for document in cursor: # iterate through each db result and append to a list
                response.append(document)
            return Response('{"response":%s,"message":"Succesfully retreived all documents"}' % dumps(response), status=200, mimetype='application/json')
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

    # This section checks if the incoming request is POST and 'Add' content into mlab db
    elif request.method == "POST":
        try:
            data = request.json # retrieve parameters
            table.insert({"name": str(data["name"]), "price": str(data["price"])}) # insert into db
            return Response('{"message":"Succesfully added."}', status=201, mimetype='application/json')
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')
    
    # This section checks if the incoming request is DELETE and 'Delete all' content from mlab db
    elif request.method == "DELETE":
        try:
            table.remove() # delete all entries in table
            return Response(status=204, mimetype='application/json')
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')


def setupDB(db, collection):
    uri = "mongodb://binoy123:binoy123@ds155634.mlab.com:55634/apifortest?retryWrites=false"
    client = pymongo.MongoClient(uri)
    db = client[db]  # identifying the db
    collection = db[collection]  # identifying the collection/table
    return collection


if __name__ == "__main__":
    app.run(debug=True)
