# Download the helper library from https://www.twilio.com/docs/python/install
import os
import argparse
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure

parser = argparse.ArgumentParser()
parser.add_argument('--phone', type=str, required=True, help='Phone number to call (e.g. +3581234567)')
args = parser.parse_args()

with open('api_keys/twilio_account_sid.txt', 'r') as f:
    account_sid = f.read().strip()
with open('api_keys/twilio_auth_token.txt', 'r') as f:
    auth_token = f.read().strip()
client = Client(account_sid, auth_token)

call = client.calls.create(
  url="https://rauha.co.uk/voice",
  to=args.phone,
  from_="+358454901439"
)

print(call.sid)