from flask_restplus import fields


def createAvailabilitySchema(api):
    availability = api.model('Availability', {
        'date': fields.String(required=True, description='The availability date xx/xx/xxxx'),
        'start-time': fields.String(required=True, description='The availability time xx:xx'),
        'end-time': fields.String(required=True, description='The availability end time'),
    })
    return availability


def createAvailabilityTimeSlotSchema(api):
    availabilityTimeSlotSchema = api.model('TimeSlotAvailability', {
        'store_id': fields.String(required=True, description='The store identifier'),
        'date': fields.String(required=True, description='The availability date xx/xx/xxxx'),
        'start-time': fields.String(required=True, description='The availability start time'),
        'end-time': fields.String(required=True, description='The availability end time'),
        'timeslot-duration': fields.Integer(required=True, description='The availability time slot duration')
    })
    return availabilityTimeSlotSchema


def deleteAvailabilitySchema(api):
    objectId = api.model('objectId', {
        "$oid": fields.String()
    })
    id = api.model('id', {
        "_id": fields.Nested(objectId)
    })
    return id
