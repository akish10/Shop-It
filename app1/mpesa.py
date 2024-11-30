import json 

import requests

from requests.auth import HTTPBasicAuth

from datetime import datetime

import base64

class Credentials:

    consumer_key = "0W8t3FfncMXmcNkTuXj8ZkUczjzASm4hVVA9Vt0MppK5GtQ4"

    consumer_ secret = "NnGxmIqGXFa7dIiu8i89LkdJ6dT9GL4u7KlYQjaISynZyE1YKjioh00j7oAJ4I21 "

    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials. 
"


class AccessToken:

    request = requests.get(Credentials.api_url, auth = HTTPBasicAuth(Credentials.consumer_key,Credentials.consumer_secret))

    access_token = request.json()['access_token']

class Passwordd:

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%')

    shortcode = '174379'

    passkey = ''



