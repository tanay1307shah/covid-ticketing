from flask_restplus import fields
from .availability import createAvailabilitySchema
from .reservation import createStoreReservationSchema


def createStoreSchema(api):
    availability = createAvailabilitySchema(api)
    reservation = createStoreReservationSchema(api)
    storeModel = api.model('Store', {
        'id_owner': fields.String(required=True, description='ID of the store owner.'),
        'location': fields.String(required=True, description='Address of the store.'),
        'name': fields.String(required=True, description='Name of the store.'),
        'phone': fields.String(required=True, description='Phone number for the store.'),
        'availability': fields.List(fields.Nested(availability, required=False, description='List of availabilities')),
        'reservations': fields.List(fields.Nested(reservation, required=False, description='List of Reservations made at the store'))
    })
    return storeModel


def createDeleteStoreSchema(api):

    deleteStoreModel = api.model('deleteStoreModel', {
        'store_id': fields.String('ID of the store.'),
    })
    return deleteStoreModel
