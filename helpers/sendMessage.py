from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACcae58d44621ec3dde4529f074ae428be"
# Your Auth Token from twilio.com/console
auth_token = "458c28a9f97e2197bc5354c04443bc52"


def sendMessage(personName, number, storeName, date, startTime, endTime, message):
    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to="+1"+number,
            from_="+12565007953",
            body="Hello," + personName + " your reservation for " + storeName +
            " from " + startTime + " till " + endTime + " on " + date + " " + message
        )
        print(message + " is sent")
    except Exception as e:
        print("Error occurred:", str(e.args))
