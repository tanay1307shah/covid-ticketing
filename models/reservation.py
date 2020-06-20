from flask_restplus import fields


def createReservationSchema(api):
    reservation = api.model('Reservation', {
        'id_customer': fields.String('ID of the store.'),
        'date': fields.Date(required=True, description='The availability date'),
        'time': fields.DateTime(required=True, description='The availability time')
    })
    return reservation


def deleteAvailabilitySchema(api):
    objectId = api.model('objectId', {
        "$oid": fields.String()
    })
    id = api.model('id', {
        "_id": fields.Nested(objectId)
    })
    return id
