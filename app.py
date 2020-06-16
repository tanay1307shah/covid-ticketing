from flask import Flask, request, Response, render_template
import pymongo
from flask_restplus import Api, Resource, fields
from bson.json_util import dumps,loads
from bson import json_util
import json
from models.store import storeSchema


app = Flask( __name__, template_folder='./client')
api = Api(app)
table = None

# storeModel = api.model('Store', {
#     'id_store' : fields.String('ID of the store.'),
#     'id_owner' : fields.String('ID of the store owner.'),
#     'location' : fields.String('Address of the store.'),
#     'name' : fields.String('Name of the store.'),
#     'phone' : fields.String('Phone number for the store.'),
#     'availability': fields.List(fields.DateTime('Time slots available')),

# })

# storeModel = api.schema.model('Store', {
#     'properties': {
#         'road': {
#             'type': 'string'
#         },
#     },
#     'type': 'object'
# })

address = storeSchema(api)
languages = []
python = {'language' : 'Python'}
languages.append(python)

@api.route('/store')
class Store(Resource):
    def get(self):
        global table
        if table is None:
            table = setupDB("covid-ticketing-db", "store")
        try:
            cursor = table.find()   # operation on table to get all data
            response = []
            for document in cursor: # iterate through each db result and append to a list
                response.append(document)
            return Response('{"response":%s,"message":"Succesfully retreived all documents"}' % dumps(response), status=200, mimetype='application/json')

        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

    @api.expect(address)
    def post(self):
        languages.append(api.payload)
        return {'result' : 'Language added'}, 201 


def setupDB(db, collection):
    uri = "mongodb://binoy123:binoy123@ds034807.mlab.com:34807/covid-ticketing-db?retryWrites=false"
    client = pymongo.MongoClient(uri)
    db = client[db]  # identifying the db
    collection = db[collection]  # identifying the collection/table
    return collection


if __name__ == "__main__":
    app.run(debug=True)
