import requests

class GenericRestClient:

    def __init__(self, headers):
        self.headers = headers

    def get(self, endpoint, params=None):
        response = requests.get(endpoint, headers=self.headers, params=params)
        return response

    def post(self, endpoint, data=None):
        response = requests.post(endpoint, headers=self.headers, json=data)
        return response

    def delete(self, endpoint):
        response = requests.delete(endpoint, headers=self.headers)
        return response