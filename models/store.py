from flask_restplus import fields
def storeSchema(api):
    availability = api.model('Availability', {
    'date': fields.Date(required=False, description='The availability date'),
    'time': fields.Date(required=False, description='The availability time')
    })

    reservation = api.model('Reservation', {
    'id_customer' : fields.String('ID of the store.'),   
    'date': fields.Date(required=False, description='The availability date'),
    'time': fields.DateTime(required=False, description='The availability time')
    })

    storeModel = api.model('Store', {
        'id_store' : fields.String('ID of the store.'),
        'id_owner' : fields.String('ID of the store owner.'),
        'location' : fields.String('Address of the store.'),
        'name' : fields.String('Name of the store.'),
        'phone' : fields.String('Phone number for the store.'),
        'availability': fields.List(fields.Nested(availability, description='List of availabilities')),
        'reservations':fields.List(fields.Nested(reservation, description='List of Reservations made at the store'))
    })
    return storeModel