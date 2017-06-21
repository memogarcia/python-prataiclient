import requests

from prataiclient.utils import create_headers_for_request


class FunctionManager(object):

    def __init__(self, client, verify=True):
        self.client = client
        self.endpoint = self.client.endpoint + '/functions'
        self.verify = verify

    @property
    def headers(self):
        return create_headers_for_request(self.client.auth_token)

    def create(self, files=None):
        r = requests.post(self.endpoint,
                          files=files,
                          headers=self.headers)
        if r.status_code != 201:
            raise Exception(r)
        return r.text

    def delete(self, function_id):
        endpoint = self.endpoint + '/' + function_id
        r = requests.delete(endpoint, headers=self.headers, verify=self.verify)
        if r.status_code != 204:
            raise Exception(r)

    def list(self):
        r = requests.get(self.endpoint, headers=self.headers,
                         verify=self.verify)
        if r.status_code != 302:
            raise Exception(r)

        return r.json()

    def get(self, function_id):
        endpoint = self.endpoint + '/' + function_id
        r = requests.get(endpoint, headers=self.headers, verify=self.verify)
        if r.status_code == 302:
            return r.json()
        if r.status_code == 404:
            return None
        raise Exception(r)

    def execute(self, function_id, payload):
        endpoint = self.endpoint + '/' + function_id
        r = requests.post(endpoint, data=payload, headers=self.headers,
                          verify=self.verify)

        if r.status_code != 202:
            raise Exception(r)
        return r.status_code

    def running_list(self):
        endpoint = self.endpoint + '/' + 'running'
        r = requests.get(endpoint, headers=self.headers,
                         verify=self.verify)
        if r.status_code != 302:
            raise Exception(r)

        return r.json()

    def stop(self, function_id):
        endpoint = self.endpoint + '/' + function_id
        r = requests.post(endpoint,
                          data=None,
                          headers=self.headers)
        if r.status_code != 202:
            raise Exception(r)
        return r.status_code
