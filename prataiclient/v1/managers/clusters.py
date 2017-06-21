import requests

from prataiclient.utils import create_headers_for_request


class ClusterManager(object):
    def __init__(self, client, verify=True):
        self.client = client
        self.endpoint = self.client.endpoint + '/cluster'
        self.verify = verify

    @property
    def headers(self):
        return create_headers_for_request(self.client.auth_token)

    def status(self):
        r = requests.get(self.endpoint, headers=self.headers,
                         verify=self.verify)
        if r.status_code != 302:
            raise Exception(r)

        return r.json()
