import requests

NAMER_URI = 'https://namey.muffinlabs.com/name.json?frequency=all'


def get_random_name(namer_uri=NAMER_URI):
    resp = requests.get(namer_uri)
    return resp.json()[0]
