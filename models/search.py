from flask_restplus import fields
def searchModel(api):
    searchModel = api.model("search",{
        "searchTerm" : fields.String(required=True,description="search term to be searched for.")
    })
    return searchModel