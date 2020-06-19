from flask_restplus import fields
def loginInfoModel(api):
    loginModel = api.model('Login', {
        'username' : fields.String(required=True, description="Username for login"),
        'password' : fields.String(required=True, description="Password for login")
    })

    return loginModel