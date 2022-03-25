import os
from twilio.rest import Client


class TextManager:
    def __init__(self):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.from_phone_number = os.environ.get("TWILIO_FROM_PHONE")
        self.to_phone_number = os.environ.get("TWILIO_TO_PHONE")
        self.client = Client(account_sid, auth_token)

    def send_message(self, msg):
        message = self.client.messages.create(
            body=msg,
            from_=self.from_phone_number,
            to=self.to_phone_number
        )

        print(message.sid)