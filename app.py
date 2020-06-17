from flask import Flask, request, Response, render_template
from flask_restplus import Api, Resource, fields
from bson.json_util import dumps,loads
from models.store import storeSchema
from helpers.setupDB import setupDB


app = Flask( __name__, template_folder='./client')
api = Api(app)

table = setupDB("covid-ticketing-db", "store")
# Generating schema for store
store = storeSchema(api)

ns_store = api.namespace('Store', description='CRUD operations for Store')

@ns_store.route('/store')
class Store(Resource):
    global table
    
    def get(self):
        try:
            cursor = table.find()   # operation on table to get all data
            response = []
            for document in cursor: # iterate through each db result and append to a list
                response.append(document)
            return Response('{"response":%s,"message":"Succesfully retreived all documents"}' % dumps(response), status=200, mimetype='application/json')

        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

    @ns_store.expect(store)
    def post(self):
        try:
            data = api.payload
            # insert into db
            inserted_docId = table.insert({
            'id_store' : data['id_store'],
            'id_owner' : data['id_owner'],
            'location' : data['location'],
            'name' : data['name'],
            'phone' : data['phone'],
            'availability': data['availability'],
            'reservations': data['reservations']
            }) 
            return Response('{"message":"Succesfully added."}', status=201, mimetype='application/json')
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True,host='127.0.0.1', port=8080)
