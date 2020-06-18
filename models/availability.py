from flask_restplus import fields

def createAvailabilitySchema(api):
    availability = api.model('Availability', {
    'date': fields.Date(required=True, description='The availability date'),
    'time': fields.Date(required=True, description='The availability time')
    })
    return availability 

def createAvailabilityTimeSlotSchema(api):
    availabilityTimeSlotSchema = api.model('Availability', {
    'date': fields.Date(required=True, description='The availability date'),
    'time': fields.Date(required=True, description='The availability time')
    })


def deleteAvailabilitySchema(api):
    objectId= api.model('objectId',{
        "$oid": fields.String()
    })
    id = api.model('id',{
        "_id": fields.Nested(objectId)
    })
    return id