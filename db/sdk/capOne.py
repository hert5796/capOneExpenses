from email import header
from requests import get, post
from json import dumps

class CapOne(object):
    def __init__(self):
        with open("./db/crd.txt", "r") as f:
            self.TKN = f.read()

        self.headers = {
            'Authorization': f'Bearer {self.TKN}',
            'Content-Type': 'application/json',
            'version': '1.0'
        }
    
    def post_request(self, endpoint, payload):
        return post(
            endpoint,
            headers=self.headers,
            data=dumps(payload)
        )

    def get_request(self, endpoint, params=None):
        return get(
            endpoint,
            headers=self.headers,
            params=params
        )