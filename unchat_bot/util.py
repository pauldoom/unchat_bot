import requests

NAMER_URI = 'http://namey.muffinlabs.com/name.json?with_surname=true'


def get_random_name(namer_uri=NAMER_URI):
    resp = requests.get(namer_uri)
    return resp.json()[0]
