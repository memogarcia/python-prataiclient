import requests

from prataiclient.utils import create_headers_for_request


class ImageManager(object):

    def __init__(self, client, verify=True):
        self.client = client
        self.endpoint = self.client.endpoint + '/images'
        self.verify = verify

    @property
    def headers(self):
        return create_headers_for_request(self.client.auth_token)

    def list(self):
        r = requests.get(self.endpoint, headers=self.headers,
                         verify=self.verify)
        if r.status_code != 302:
            raise Exception(r)

        return r.json()

    def get(self, image_id):
        endpoint = self.endpoint + '/' + image_id
        r = requests.get(endpoint, headers=self.headers, verify=self.verify)
        if r.status_code == 302:
            return r.json()
        if r.status_code == 404:
            return None
        raise Exception(r)

    def create(self, files=None):
        r = requests.post(self.endpoint,
                          files=files,
                          headers=self.headers)
        if r.status_code != 202:
            raise Exception(r)
        return r.text

    def delete(self, image_id):
        endpoint = self.endpoint + '/' + image_id
        r = requests.delete(endpoint, headers=self.headers, verify=self.verify)
        if r.status_code != 204:
            raise Exception(r)
