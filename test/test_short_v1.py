from unittest import TestCase
import json

from vs.database.exception import IdNotFound
from vs import create_application


class ShortV1ApiTest(TestCase):
    API_ENDPOINT = '/api/v1/short'

    def setUp(self):
        self.app = create_application()
        self.app.config.from_object('test.short_v1_config')
        self.app.config['DATABASE'].init_app(self.app)
        self.app.debug = True
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def client_put(self):
        response = self.client.put('/api/v1/short', data={
            'url': 'http://github.com',
            'expire': 3,
            'id': 'customid'
        })
        assert response.status_code == 200, response.data
        j = json.loads(response.data.decode('utf-8'))
        assert j['id'] == 'customid'

        response = self.client.put(self.API_ENDPOINT, data={
            'url': 'http://gist.github.com'
        })
        assert response.status_code == 200, response.data
        j = json.loads(response.data.decode('utf-8'))

        return j['id'], j['secret']

    def client_get(self, id):
        response = self.client.get(self.API_ENDPOINT, data={
            'id': 'customid'
        })
        assert response.status_code == 200, response.data
        j = json.loads(response.data.decode('utf-8'))
        assert j['url'] == 'http://github.com'

        response = self.client.get(self.API_ENDPOINT, data={
            'id': id
        })
        assert response.status_code == 200, response.data

    def client_delete(self, id, secret):
        response = self.client.delete(self.API_ENDPOINT, data={
            'id': id,
            'secret': secret
        })
        assert response.status_code == 200, response.data

        try:
            self.client.get(self.API_ENDPOINT, data={'id': id})
        except IdNotFound:
            pass
        else:
            assert False

    def test_short(self):
        id, secret = self.client_put()
        self.client_get(id)
        self.client_delete(id, secret)
