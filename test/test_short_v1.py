# encoding: utf-8

from unittest import TestCase
import json

from vs.database.exception import IdNotFound, InvalidId, InvalidUrl
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

    def test_invalid_id(self):
        response = self.client.put(self.API_ENDPOINT, data={
            'url': 'http://github.com',
            'id': 'customid+'
        })
        self.assertTrue(response.status_code == 400)

    def test_invalid_url(self):
        for url in ('I am not an url', 'http://'):
            response = self.client.put(self.API_ENDPOINT, data={
                'url': 'I am not an url',
            })
            self.assertTrue(response.status_code == 400, 'Allowed invalid Url')

    def client_put(self):
        response = self.client.put(self.API_ENDPOINT, data={
            'url': 'http://github.com',
            'expiry': 3,
            'id': 'customid'
        })
        self.assertTrue(response.status_code == 200)
        j = json.loads(response.data.decode('utf-8'))
        self.assertTrue(j['id'] == 'customid')

        response = self.client.put(self.API_ENDPOINT, data={
            'url': 'http://gist.github.com'
        })
        self.assertTrue(response.status_code == 200)
        j = json.loads(response.data.decode('utf-8'))

        return j['id'], j['secret']

    def client_get(self, id):
        response = self.client.get(self.API_ENDPOINT, data={
            'id': 'customid'
        })
        self.assertTrue(response.status_code == 200)
        j = json.loads(response.data.decode('utf-8'))
        self.assertTrue(j['url'] == 'http://github.com')

        response = self.client.get(self.API_ENDPOINT, data={
            'id': id
        })
        self.assertTrue(response.status_code == 200)

    def client_delete(self, id, secret):
        response = self.client.delete(self.API_ENDPOINT, data={
            'id': id,
            'secret': secret
        })
        self.assertTrue(response.status_code == 200)

        response = self.client.get(self.API_ENDPOINT, data={'id': id})
        self.assertTrue(response.status_code == 404, 'Id still exists')

    def test_short(self):
        id, secret = self.client_put()
        self.client_get(id)
        self.client_delete(id, secret)
