from flask import Flask, request, Response, render_template, url_for
from flask_restplus import Api, Resource, fields,marshal_with
from bson.json_util import dumps,loads
from models.store import createStoreSchema, deleteStoreSchema
from models.customer import createCustomerSchema, deleteCustomerSchema, getCustomerSchema
from models.login import loginInfoModel
from helpers.setupDB import setupDB
from passlib.hash import pbkdf2_sha256
import os
import sys


app = Flask( __name__, template_folder='./client')

# This function make sure that swagger UI works when deployed onto a https server
if os.environ.get('NPM_MIRROR'):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')
    Api.specs_url = specs_url
api = Api(app)

table = setupDB("covid-ticketing-db", "store")
customerTable = setupDB("covid-ticketing-db","customer")
ns_api_v1 = api.namespace('api/v1', description='CRUD operations for Store')

@ns_api_v1.route('/store')
class Store(Resource):
    global table
   # @marshal_with(store_marshal)
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

            

    @ns_api_v1.expect(createStoreSchema(api))
    def post(self):
        try:
            data = api.payload
            # insert into db
            inserted_docId = table.insert_one({
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
            deleted_docId = table.delete_one(loads(dumps(api.payload)))
            if deleted_docId.deleted_count:
                return  {'message':'Succesffuly deleted.'}, 204
            return {'message':'Cannot perform the operation as there are no documents with the provided id.'}, 200
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')


@ns_api_v1.route('/customer')
class Customer(Resource):
    global customerTable
   # @marshal_with(store_marshal)

    def get(self):
        try:
            cursor = customerTable.find({}, {"password" : 0})   # operation on table to get all data
            response = []
            for document in cursor: # iterate through each db result and append to a list
                response.append(document)
            return Response('{"response":%s,"message":"Succesfully retreived all documents"}' % dumps(response), status=200, mimetype='application/json')


        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')            


    @ns_api_v1.expect(createCustomerSchema(api))
    def post(self):
        try:
            data = api.payload
            hash = pbkdf2_sha256.hash(data['password'])
       
            # insert into db
            inserted_docId = customerTable.insert_one({
            'name' : data['name'],
            'phone' : data['phone'],
            'username' : data['username'],
            'password' : hash
            }) 
            return Response('{"message":"Succesfully added.","_id":%s}' % dumps(inserted_docId.inserted_id), status=201, mimetype='application/json')
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

@ns_api_v1.route('/customer/login')
class customerLogin(Resource):
    global customerTable

    @ns_api_v1.expect(loginInfoModel(api))
    def post(self):
        try:
            data = api.payload
            
            cursor = customerTable.find({"username" : data['username']})
            
            response = []
            for document in cursor: # iterate through each db result and append to a list
                response.append(document)
            print(response)
            if response != [] and pbkdf2_sha256.verify(data['password'],response[0]['password']):
                return Response('{"response":"Authorized"}', status=200, mimetype='application/json')
            return Response('{"response":"Unauthorized"}', status=401, mimetype='application/json')
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=8080)
