from flask_restplus import fields

def createOwnerSchema(api):

    owner = api.model("owner",{
        'username': fields.String(required=True, description='Username for the vendor/owner.'),
        'name': fields.String(required=True, description='Name of the vendor/owner.'),
        'phone': fields.String(required=True, description='Phone number for the vendor/owner.'),
        'password': fields.String(required=True, description='Password for the owner/vendor.'),
    })
    return owner


def createDeleteOwnerSchema(api):

    objectId = api.model('objectId', {
        "$oid": fields.String()
    })
    id = api.model('id', {
        "_id": fields.Nested(objectId)
    })
    return id
