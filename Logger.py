import os
from datetime import datetime
import logging
from twilio.rest import Client


def send_alert(msg):
    print(msg)
    account_sid = os.environ['account_sid']
    auth_token = os.environ['auth_token']
    from_phone = os.environ['phone']
    phoneNumbers = os.environ['phone_numbers'].split(' ')

    if not all([account_sid, auth_token, from_phone]):
        return   logging.info("Setup a trilio account to use this feature")

    client = Client(account_sid, auth_token)
    messages = []
    for number in phoneNumbers:
        messages.append(client.messages.create(
            body=f'{msg}',
            from_=from_phone,
            to='+1' + number
        ))
        logging.info(f"SMS sent to {number}")
