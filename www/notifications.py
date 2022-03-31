import os
#from twilio.rest import Client


# account_sid = os.getenv('TWILIO_API_SID')
# auth_token = os.getenv('TWILIO_API_KEY')
# client = Client(account_sid, auth_token)

from textmagic.rest import TextmagicRestClient
username = os.getenv('TEXTMAGIC_USERNAME')
token = os.getenv('TEXTMAGIC_API_KEY')
client = TextmagicRestClient(username, token)

message = client.messages.create(
    phones="447918813886",
    text="Hello - test test"
)
