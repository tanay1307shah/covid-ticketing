from flask_restplus import fields


def createReservationSchema(api):
    reservation = api.model('Reservation', {
        'store_id': fields.String('ID of the store.'),
        'customer_id': fields.String('ID of the customer.'),
        'date': fields.Date(required=True, description='The reservation date'),
        'start-time': fields.DateTime(required=True, description='The reservation start time'),
        'end-time': fields.DateTime(required=True, description='The reservation end time')
    })
    return reservation


def createStoreReservationSchema(api):
    storeReservation = api.model('StoreReservation', {
        'customer_id': fields.String('ID of the customer.'),
        'date': fields.Date(required=True, description='The reservation date'),
        'start-time': fields.DateTime(required=True, description='The reservation start time'),
        'end-time': fields.DateTime(required=True, description='The reservation end time')
    })
    return storeReservation


def createCustomerReservationSchema(api):
    customerReservation = api.model('CustomerReservation', {
        'store_id': fields.String('ID of the store.'),
        'date': fields.Date(required=True, description='The reservation date'),
        'start-time': fields.DateTime(required=True, description='The reservation start time'),
        'end-time': fields.DateTime(required=True, description='The reservation end time')
    })
    return customerReservation


def deleteAvailabilitySchema(api):
    objectId = api.model('objectId', {
        "$oid": fields.String()
    })
    id = api.model('id', {
        "_id": fields.Nested(objectId)
    })
    return id
