from flask_restplus import fields

def reservationSchema(api):
    reservation = api.model('Reservation', {
        'id_store' : fields.String('ID of the store.'),   
        'date': fields.Date(required=True, description='The availability date'),
        'time': fields.DateTime(required=True, description='The availability time')
    })
    return reservation
