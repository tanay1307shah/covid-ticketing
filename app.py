from flask import Flask, request, Response, render_template, url_for
from flask_restplus import Api, Resource, fields,marshal_with
from bson.json_util import dumps,loads
from models.store import createStoreSchema, deleteStoreSchema
from models.availability import createAvailabilitySchema
from helpers.setupDB import setupDB
import os


app = Flask( __name__, template_folder='./client')

# This function make sure that swagger UI works when deployed onto a https server
if os.environ.get('NPM_MIRROR'):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')
    Api.specs_url = specs_url
api = Api(app)

table = setupDB("covid-ticketing-db", "store")
ns_api_v1 = api.namespace('api/v1', description='CRUD operations for Store')

@ns_api_v1.route('/store')
class Store(Resource):
    global table
   # @marshal_with(store_marshal)
    def get(self):
        try:
            cursor = table["store"].find()   # operation on table to get all data
            response = []
            for document in cursor: # iterate through each db result and append to a list
                response.append(document)
            return Response('{"response":%s,"message":"Successfully retreived all documents"}' % dumps(response), status=200, mimetype='application/json')

        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

    @ns_api_v1.expect(createStoreSchema(api))
    def post(self):
        try:
            data = api.payload
            # insert into db
            inserted_docId = table["store"].insert_one({
            'id_owner' : data['id_owner'],
            'location' : data['location'],
            'name' : data['name'],
            'phone' : data['phone'],
            'availability': data['availability'],
            'reservations': data['reservations']
            }) 
            return Response('{"message":"Successfully added.","_id":%s}' % dumps(inserted_docId.inserted_id), status=201, mimetype='application/json')
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

    @ns_api_v1.response(204, 'Store deleted')
    @ns_api_v1.expect(deleteStoreSchema(api))
    def delete(self):
        try:
            deleted_docId = table["store"].delete_one(loads(dumps(api.payload)))
            if deleted_docId.deleted_count:
                return  {'message':'Succesffuly deleted.'}, 204
            return {'message':'Cannot perform the operation as there are no documents with the provided id.'}, 200
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

@ns_api_v1.route('/availability')
class Availability(Resource):
    global table
    def get(self):
        try:
            cursor = table["store"].find()   # operation on table to get all data
            response = []
            for document in cursor: # iterate through each db result and append to a list
                response.append(document)
            return Response('{"response":%s,"message":"Succesfully retrieved all documents"}' % dumps(response), status=200, mimetype='application/json')

        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

    @ns_api_v1.expect(createAvailabilitySchema(api))
    def post(self):
        try:
            data = api.payload
            # insert into db
            inserted_docId = table["store"].insert_one({
            'id_owner' : data['id_owner'],
            'location' : data['location'],
            'name' : data['name'],
            'phone' : data['phone'],
            'availability': data['availability'],
            'reservations': data['reservations']
            }) 
            return Response('{"message":"Succesfully added.","_id":%s}' % dumps(inserted_docId.inserted_id), status=201, mimetype='application/json')
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

    @ns_api_v1.response(204, 'Store deleted')
    @ns_api_v1.expect(deleteStoreSchema(api))
    def delete(self):
        try:
            deleted_docId = table["store"].delete_one(loads(dumps(api.payload)))
            if deleted_docId.deleted_count:
                return  {'message':'Succesffuly deleted.'}, 204
            return {'message':'Cannot perform the operation as there are no documents with the provided id.'}, 200
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=8080)
