import json 

import requests

from requests.auth import HTTPBasicAuth

from datetime import datetime

import base64

class Credentials:

    consumer_key = "0W8t3FfncMXmcNkTuXj8ZkUczjzASm4hVVA9Vt0MppK5GtQ4"

    consumer_secret = "NnGxmIqGXFa7dIiu8i89LkdJ6dT9GL4u7KlYQjaISynZyE1YKjioh00j7oAJ4I21 "

    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"


class AccessToken:

    request = requests.get(Credentials.api_url, auth = HTTPBasicAuth(Credentials.consumer_key,Credentials.consumer_secret))

    access_token = json.loads(request.text)['access_token']

class Passwordd:

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%')

    shortcode = '174379'

    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    to_encode = shortcode + passkey + timestamp 

    encoded_password = base64.b64encode(to_encode.encode())

    decoded_password = encoded_password.decode('utf-8')





    