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


def createDeleteReservationSchema(api):
    deleteReservationSchema = api.model('deleteReservation', {
        'store_id': fields.String(required=True, description='Id of the store'),
        'customer_id': fields.String(required=True, description='Id of the store'),
        'date': fields.String(required=True, description='The availability date xx/xx/xxxx'),
        'start-time': fields.String(required=True, description='The availability start time'),
        'end-time': fields.String(required=True, description='The availability end time')
    })
    return deleteReservationSchema
