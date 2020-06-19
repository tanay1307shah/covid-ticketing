import sys
def getLastCustomerId(collection):
    try:
        cursor = collection.find()   # operation on table to get all data
        response = []
        for document in cursor: # iterate through each db result and append to a list
            response.append(document)
        if response != []:
            return response[-1]["id"]
        else:
            return 0

    except Exception as e:
        print("Error occured:", str(e.args))
        return sys.maxsize