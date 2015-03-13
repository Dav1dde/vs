# encoding: utf-8

from unittest import TestCase
import json

from test.client import APIv1Client

from vs.database.exception import IdNotFound, InvalidId, InvalidUrl
from vs import create_application


class ShortV1ApiTest(TestCase):
    def setUp(self):
        self.app = create_application()
        self.app.config.from_object('test.vs_config')
        self.app.config['DATABASE'].init_app(self.app)
        self.app.debug = True
        self.api = APIv1Client(self.app)

    def tearDown(self):
        pass

    def test_invalid_id(self):
        j = self.api.short.put(
            {'url': 'http://github.com', 'id': 'customid+'}, expected=400
        )

    def test_invalid_url(self):
        for url in ('I am not an url', 'http://'):
            j = self.api.short.put({'url': 'I am not an url'}, expected=400)

    def client_put(self):
        j = self.api.short.put(
            {'url': 'http://github.com', 'expiry': 3, 'id': 'customid'}
        )
        self.assertTrue(j['id'] == 'customid')

        j = self.api.short.put({'url': 'http://gist.github.com'})
        return j['id'], j['secret']

    def client_get(self, id):
        j = self.api.short.get({'id': 'customid'})
        self.assertTrue(j['url'] == 'http://github.com')

        j = self.api.short.get(data={'id': id})
        self.assertTrue(j['url'] == 'http://gist.github.com')

    def client_delete(self, id, secret):
        self.api.short.delete({'id': id, 'secret': secret})
        self.api.short.get({'id': id}, expected=404)

    def test_short(self):
        id, secret = self.client_put()
        self.client_get(id)
        self.client_delete(id, secret)
