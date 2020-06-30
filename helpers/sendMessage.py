from twilio.rest import Client


def sendMessage(db,personName, number, storeName, date, startTime, endTime, message):
    
    twilio_credentials = db['twilio_credentials'].find_one()
    
    account_sid = twilio_credentials['account_sid']
    auth_token = twilio_credentials['auth_token']
    from_number = twilio_credentials['from_number']
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to="+1"+number,
            from_= from_number,
            body="Hello," + personName + " your reservation for " + storeName +
            " from " + startTime + " till " + endTime + " on " + date + " " + message
        )
        print(message + " is sent")
    except Exception as e:
        print("Error occurred:", str(e.args))
