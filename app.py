from flask import Flask, request, Response, render_template, url_for
from flask_restplus import Api, Resource, fields, marshal_with
from bson.json_util import dumps, loads
from bson import ObjectId

from models.store import createStoreSchema, createDeleteStoreSchema
from models.availability import createAvailabilitySchema, createAvailabilityTimeSlotSchema, createDeleteAvailabilitySchema
from models.reservation import createReservationSchema, createDeleteReservationSchema
from models.owner import createOwnerSchema, createDeleteOwnerSchema


from helpers.setupDB import setupDB
from helpers.time import timeSlotDurations, stringTimeToMinutes, minutesToStringTime
from models.customer import createCustomerSchema, createDeleteCustomerSchema
from models.login import loginInfoModel
from helpers.setupDB import setupDB
from passlib.hash import pbkdf2_sha256


import os

app = Flask(__name__, template_folder='./client')

# This function make sure that swagger UI works when deployed onto a https server
if os.environ.get('NPM_MIRROR'):
    @property
    def specs_url(self):
        return url_for(self.endpoint('specs'), _external=True, _scheme='https')
    Api.specs_url = specs_url
api = Api(app)

db = setupDB("covid-ticketing-db")

STORE_TABLE = "store"
CUSTOMER_TABLE = "customer"
OWNER_TABLE = "owner"


ns_api_v1 = api.namespace('api/v1', description='CRUD operations for Store')


@ns_api_v1.route('/store')
class Store(Resource):
    global db
   # @marshal_with(store_marshal)

    def get(self):

        try:
            # operation on table to get all data
            cursor = db["store"].find()
            response = []
            for document in cursor:  # iterate through each db result and append to a list
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
            inserted_docId = db["store"].insert_one({
                'id_owner': data['id_owner'],
                'location': data['location'],
                'name': data['name'],
                'phone': data['phone'],
                'availability': data['availability'],
                'reservations': data['reservations']
            })
            return Response('{"message":"Successfully added.","_id":%s}' % dumps(inserted_docId.inserted_id), status=201, mimetype='application/json')
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

    @ns_api_v1.response(204, 'Store deleted')
    @ns_api_v1.expect(createDeleteStoreSchema(api))
    def delete(self):
        try:
            customerIdsWithReservations = []
            selectedStore = ""
            # find the store that needs to be deleted
            selectedStore = db["store"].find_one(
                {"_id": ObjectId(api.payload['store_id'])})
            if selectedStore:
                # find reservations of customerids that needs to be deleted
                for reservation in selectedStore['reservations']:
                    customerIdsWithReservations.append(
                        reservation['customer_id'])
                # delete those reservations of the store from customer table
                for customerId in customerIdsWithReservations:
                    customer = db['customer'].find_one(
                        {'_id': ObjectId(customerId)})
                    for reservation in customer['reservations']:
                        if reservation['store_id'] == api.payload['store_id']:
                            db["customer"].update({
                                '_id': ObjectId(customerId),
                            }, {
                                '$pull': {"reservations": {
                                    "date": reservation['date'],
                                    "start-time": reservation['start-time'],
                                    "end-time": reservation['end-time'],
                                    "store_id": reservation['store_id']
                                }}
                            })
                # Now that all the reservations are deleted from customer table, safely delete the store
                deleted_docId = db["store"].delete_one(
                    {'_id': ObjectId(api.payload['store_id'])})
                if deleted_docId.deleted_count:
                    return {'message': 'Succesffuly deleted.'}, 204
            return {'message': 'Cannot perform the operation as there is no store with the provided id.'}, 200
        except Exception as e:
            print("Error occurred:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')


@ns_api_v1.route('/availability')
class Availability(Resource):
    global db

    def get(self):
        try:
            # operation on table to get all data
            cursor = db["store"].find()
            response = []
            for document in cursor:  # iterate through each db result and append to a list
                response.append(document)
            return Response('{"response":%s,"message":"Succesfully retrieved all documents"}' % dumps(response), status=200, mimetype='application/json')

        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

    @ns_api_v1.expect(createAvailabilityTimeSlotSchema(api))
    def post(self):
        try:
            data = api.payload
            # this list stores set of all timeslots between chosen start time and end time
            availability = []
            total_minutes = stringTimeToMinutes(
                data['end-time']) - stringTimeToMinutes(data['start-time'])
            start_time_mins = stringTimeToMinutes(data['start-time'])
            for x in range(0, total_minutes//int(data['timeslot-duration'])):
                availability.append({
                    'date': data['date'],
                    'start-time': minutesToStringTime(start_time_mins),
                    'end-time': minutesToStringTime(start_time_mins + int(data['timeslot-duration'])),
                })
                start_time_mins = start_time_mins + \
                    int(data['timeslot-duration'])

            selectedStore = ""
            cursor = db["store"].find({"_id": ObjectId(data['store_id'])})
            for doc in cursor:
                selectedStore = doc
            bDuplicateItemFound = False
            # check if availability for the store is empty as of now
            if selectedStore['availability'] is not None:
                for element in availability:
                    bDuplicateItemFound = False
                    for item in selectedStore['availability']:
                        # only add availability timeslots which are not already existing
                        if ((element['date'] == item['date'] and element['start-time'] == item['start-time'] and element['end-time'] == item['end-time'])):
                            bDuplicateItemFound = True
                            break
                    if not(bDuplicateItemFound):
                        selectedStore['availability'].append(element)

            # update the store with sorted availability
                result = db["store"].update_one({
                    "_id": ObjectId(data['store_id'])
                }, {"$set": {
                    "availability": sorted(selectedStore['availability'], key=lambda elem: "%s %s" % (elem['date'], elem['start-time']))
                }}, upsert=False)
            else:
                result = db["store"].update_one({
                    "_id": ObjectId(data['store_id'])
                }, {"$set": {
                    "availability": availability
                }}, upsert=False)

            return Response('{"message":"Succesfully added.","result":%s}' % dumps(availability), status=201, mimetype='application/json')
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

    @ns_api_v1.response(204, 'Availability deleted')
    @ns_api_v1.expect(createDeleteAvailabilitySchema(api))
    def delete(self):
        try:
            data = api.payload
            result = db["store"].update({
                '_id': ObjectId(data['store_id']),
            }, {
                '$pull': {"availability": {
                    "date": data['date'],
                    "start-time": data['start-time'],
                    "end-time": data['end-time']
                }}
            })
            return {'message': 'Availability deleted successfully.'}, 204
        except Exception as e:
            print("Error occurred:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')


@ns_api_v1.route('/reservations')
class Reservations(Resource):
    global db

    @ns_api_v1.expect(createReservationSchema(api))
    def post(self):
        try:
            data = api.payload
            selectedStore = ""
            selectedCustomer = ""
            cursor = db["store"].find({"_id": ObjectId(data['store_id'])})
            for doc in cursor:
                selectedStore = doc
            cursor = db["customer"].find(
                {"_id": ObjectId(data['customer_id'])})
            for doc in cursor:
                selectedCustomer = doc

            bDuplicateItemFound = False
            for reservation in selectedStore['reservations']:
                # only add reservation timeslots which are not already existing
                if ((reservation['date'] == data['date'] and reservation['start-time'] == data['start-time'] and reservation['end-time'] == data['end-time'])):
                    bDuplicateItemFound = True
                    break
            # Only push the reservation if there are no duplicates
            if not(bDuplicateItemFound):
                # push the reservation to store table
                result = db["store"].update({
                    '_id': ObjectId(data['store_id']),
                }, {
                    '$push': {"reservations": {
                        "customer_id": data['customer_id'],
                        "date": data['date'],
                        "start-time": data['start-time'],
                        "end-time": data['end-time']
                    }}
                })
                # push the reservation to customer table
                result = db["customer"].update({
                    '_id': ObjectId(data['customer_id']),
                }, {
                    '$push': {"reservations": {
                        "store_id": data['store_id'],
                        "date": data['date'],
                        "start-time": data['start-time'],
                        "end-time": data['end-time']
                    }}
                })
                return Response('{"message":"Successfully saved the reservation."}', status=201, mimetype='application/json')
            else:
                return Response('{"message":"Could not save the reservation as a duplicate entry was found."}', status=201, mimetype='application/json')

        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

    @ns_api_v1.response(204, 'Store deleted')
    @ns_api_v1.expect(createDeleteReservationSchema(api))
    def delete(self):
        try:
            data = api.payload

            delete_store_reservation_result = db["store"].update({
                '_id': ObjectId(data['store_id']),
            }, {
                '$pull': {"reservations": {
                    "date": data['date'],
                    "start-time": data['start-time'],
                    "end-time": data['end-time'],
                    "customer_id": data['customer_id']
                }}
            })

            delete_customer_reservation_result = db["customer"].update({
                '_id': ObjectId(data['customer_id']),
            }, {
                '$pull': {"reservations": {
                    "date": data['date'],
                    "start-time": data['start-time'],
                    "end-time": data['end-time'],
                    "store_id": data['store_id']
                }}
            })
            # If one document is modified
            if(int(delete_store_reservation_result['nModified']) and int(delete_customer_reservation_result['nModified'])):
                return {'message': 'Successfully deleted the reservation.'}, 204

            return {'message': 'Cannot perform the operation as there are no reservations with requested details.'}, 200

        except Exception as e:
            print("Error occurred:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')


@ns_api_v1.route('/customer/<id>')
@ns_api_v1.doc(params={'id': 'customer_id'})
class CustomerData(Resource):
    global db
   # @marshal_with(store_marshal)

    def get(self, id):
        try:
            # operation on table to get all data
            cursor = db['customer'].find_one(ObjectId(id), {"password": 0})
            response = cursor
            return Response('{"response":%s,"message":"Succesfully retreived all documents"}' % dumps(response), status=200, mimetype='application/json')

        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')


@ns_api_v1.route('/customer')
class Customer(Resource):
    global db

    def get(self):
        try:
            # operation on table to get all data
            cursor = db['customer'].find({}, {"password": 0})
            response = []
            for document in cursor:  # iterate through each db result and append to a list
                response.append(document)
            return Response('{"response":%s,"message":"Succesfully retreived all documents"}' % dumps(response), status=200, mimetype='application/json')

        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

    @ns_api_v1.expect(createCustomerSchema(api))
    def post(self):
        try:
            data = api.payload
            # insert into db
            if not db['owner'].find_one({"username": data['username']}):
                inserted_docId = db['customer'].insert_one({
                    'name': data['name'],
                    'phone': data['phone'],
                    'username': data['username'],
                    'password': pbkdf2_sha256.hash(data['password']),
                    'reservations': []
                })
                return Response('{"message":"Succesfully added.","_id":%s}' % dumps(inserted_docId.inserted_id), status=201, mimetype='application/json')
            return Response('{"message":"Username already exists"}', status=200, mimetype='application/json')

        except Exception as e:
            print("Error occured:", str(e.args))
            if str(e.args).find("duplicate key error") > -1:
                return Response('{"message":"Username already used. Please provide a different username."}', status=400, mimetype='application/json')
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')


@ns_api_v1.route('/owner')
class Owner(Resource):
    global db

    def get(self):
        try:
            # operation on table to get all data
            cursor = db['owner'].find({}, {"password": 0})
            response = []
            for document in cursor:  # iterate through each db result and append to a list
                response.append(document)
            return Response('{"response":%s,"message":"Succesfully retreived all documents"}' % dumps(response), status=200, mimetype='application/json')

        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')

    @ns_api_v1.expect(createOwnerSchema(api))
    def post(self):
        try:
            data = api.payload
            if not db['owner'].find_one({"username": data['username']}):
                inserted_docId = db['owner'].insert_one({
                    'name': data['name'],
                    'phone': data['phone'],
                    'username': data['username'],
                    'password': pbkdf2_sha256.hash(data['password']),
                })
                return Response('{"message":"Succesfully added.","_id":%s}' % dumps(inserted_docId.inserted_id), status=201, mimetype='application/json')
            return Response('{"message":"Username already exists"}', status=200, mimetype='application/json')

        except Exception as e:
            print("Error occured:", str(e.args))
            if str(e.args).find("duplicate key error") > -1:
                return Response('{"message":"Username already used. Please provide a different username."}', status=400, mimetype='application/json')
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')


@ns_api_v1.route('/availability/<id>')
@ns_api_v1.doc(params={'id': 'owner_id'})
class OwnerAvailability(Resource):
    global db

    def get(self, id):
        try:
            # operation on table to get all data
            response = []
            cursor = db['store'].find(
                {'id_owner': id}, {"id_owner": 0, "reservations": 0})
            for doc in cursor:
                response.append(doc)
            return Response('{"response":%s,"message":"Succesfully retreived all documents"}' % dumps(response), status=200, mimetype='application/json')

        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')


@ns_api_v1.route('/login/<type>')
@ns_api_v1.doc(params={'type': 'owner or customer'})
class OwnerLogin(Resource):
    global db

    @ns_api_v1.expect(loginInfoModel(api))
    def post(self, type):
        try:
            data = api.payload
            cursor = db[type.lower()].find_one({"username": data['username']})
            response = cursor
            if response != None and pbkdf2_sha256.verify(data['password'], response['password']):
                return Response('{"response":"Authorized","_id": %s}' % dumps(response['_id']), status=200, mimetype='application/json')
            return Response('{"response":"Unauthorized"}', status=401, mimetype='application/json')
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')


@ns_api_v1.route('/search')
@ns_api_v1.doc(params={'searchTerm': {'description': 'Term to search', 'in': 'query', 'type': 'string'}})
class Search(Resource):
    global db

    def get(self):
        try:
          # operation on table to get all data
            cursor = db['store'].find(
                {"$text": {"$search": dumps(request.args.get('searchTerm'))}})
            response = []
            for document in cursor:  # iterate through each db result and append to a list
                response.append(document)
            return Response('{"response":%s,"message":"Succesfully retreived all documents"}' % dumps(response), status=200, mimetype='application/json')
        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')


@ns_api_v1.route('/reservations/<type>/<id>')
@ns_api_v1.doc(params={'type': 'Customer or owner', 'id': 'Id of owner or customer'})
class RetreiveReservations(Resource):
    global db

    def get(self, type, id):
        try:
            if(type.lower() == "customer"):
                selectedCustomer = db[type.lower()].find_one(
                    {"_id": ObjectId(id)})
                if(selectedCustomer):
                    return Response('{"response":%s,"message":"Succesfully retreived all documents"}' % dumps(selectedCustomer['reservations']), status=200, mimetype='application/json')
            elif(type.lower() == "owner"):
                response = []
                # finds stores owned by owner
                storesOwnedByOwner = db["store"].find(
                    {"id_owner": id})
                if(storesOwnedByOwner.count()):
                    storeIndex = 0
                    # for each store owned by owner add store details to response along with reservations
                    for store in storesOwnedByOwner:
                        response.append(
                            {
                                "id_store": str(store["_id"]),
                                "name": store["name"],
                                "location": store["location"],
                                "phone": store["phone"],
                                "reservations": store["reservations"]
                            })
                        # for each reservation add a new key customer_name and get it value from customer db
                        for idx in range(len(store["reservations"])):
                            # for each customer in reservation find its name
                            customer = db["customer"].find_one(
                                {"_id": ObjectId(store["reservations"][idx]["customer_id"])})
                            # modify the corresponding reservation object in response and update it with a new key customer_name
                            if(str(ObjectId(customer["_id"])) == response[storeIndex]["reservations"][idx]["customer_id"]):
                                response[storeIndex]["reservations"][idx].update(
                                    {"customer_name": customer['name']})
                        storeIndex = storeIndex+1
                    return Response('{"response":%s,"message":"Succesfully retreived all documents"}' % dumps(response), status=200, mimetype='application/json')
            return Response('{"message":"Cannot find any reservations."}', status=200, mimetype='application/json')

        except Exception as e:
            print("Error occured:", str(e.args))
            return Response('{"message":"Server error. Please check logs."}', status=400, mimetype='application/json')


# -----------Serve front end file ---------------------------

@app.route("/home")
def renderHomePage():
    return render_template('index.html')


@app.route("/customerReservations/<id>")
def renderCustomerReservations(id):
    customer_id = id
    return render_template('CustomerReservations.html', id=customer_id)


@app.route("/signup")
def renderSignUp():
    return render_template('signUp.html')


@app.route("/customerAvailability/<id>")
def renderCustomerAvailability(id):
    customer_id = id
    return render_template('CustomerAvailability.html', id=customer_id)


@app.route("/ownerStores/<id>")
def renderOwnerStores(id):
    owner_id = id
    return render_template('OwnerStores.html', id=owner_id)


@app.route("/ownerAvailability/<id>")
def renderOWnerAvailability(id):
    owner_id = id
    return render_template('OwnerAvailability.html', id=owner_id)


@app.route("/ownerReservations/<id>")
def renderOwnerReseervations(id):
    owner_id = id
    return render_template('OwnerReservations.html', id=owner_id)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
