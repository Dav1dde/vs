from werkzeug.test import Client
import json


class APIEndpoint(object):
    def __init__(self, endpoint, client):
        self.endpoint = endpoint
        self.client = client

    def _make_request(func):
        def _requester(self, data, expected=200):
            response = func(self.client, self.endpoint, data=data)
            if not response.status_code == expected:
                try:
                    j = json.loads(response.data.decode('utf-8'))
                except ValueError:
                    j = None

                msg = (
                    'Endpoint: {0}\n'
                    'Method: {1}\n'
                    'Data: {2!r}\n'
                    'Returned: {3!r}\n'
                    'Status code {4}, expected {5}'
                ).format(
                    self.endpoint, func.__name__, data,
                    j, response.status_code, expected
                )
                assert False, msg

            j = json.loads(response.data.decode('utf-8'))
            return j
        return _requester

    get = _make_request(Client.get)
    patch = _make_request(Client.patch)
    post = _make_request(Client.post)
    head = _make_request(Client.head)
    put = _make_request(Client.put)
    delete = _make_request(Client.delete)


class APIv1Client(object):
    def __init__(self, app=None):
        self.short = None
        self.domain = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.short = APIEndpoint('/api/v1/short', app.test_client())
        self.domain = APIEndpoint('/api/v1/domain', app.test_client())
