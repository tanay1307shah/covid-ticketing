from flask_restplus import fields
def createStoreSchema(api):
    availability = api.model('Availability', {
    'date': fields.Date(required=True, description='The availability date'),
    'time': fields.Date(required=True, description='The availability time')
    })

    reservation = api.model('Reservation', {
    'id_customer' : fields.String('ID of the store.'),   
    'date': fields.Date(required=True, description='The availability date'),
    'time': fields.DateTime(required=True, description='The availability time')
    })

    storeModel = api.model('Store', {
        'id_owner' : fields.String(required=True,description='ID of the store owner.'),
        'location' : fields.String(required=True,description='Address of the store.'),
        'name' : fields.String(required=True,description='Name of the store.'),
        'phone' : fields.String(required=True,description='Phone number for the store.'),
        'availability': fields.List(fields.Nested(availability, required=False,description='List of availabilities')),
        'reservations':fields.List(fields.Nested(reservation, required=False, description='List of Reservations made at the store'))
    })
    return storeModel 

def deleteStoreSchema(api):

    objectId= api.model('objectId',{
        "$oid": fields.String()
    })
    id=api.model('id',{
        "_id": fields.Nested(objectId)
    })
    return id