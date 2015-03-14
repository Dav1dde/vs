# encoding: utf-8

import json

from test.client import APIv1Client
from test.case import VSTestCase

from vs.database.exception import IdNotFound, InvalidId, InvalidUrl


class ShortV1Tests(object):
    def test_invalid_id(self):
        j = self.api.short.put(
            {'url': 'http://github.com', 'id': 'customid+'}, expected=400
        )

    def test_invalid_url(self):
        for url in ('I am not an url', 'http://'):
            j = self.api.short.put({'url': 'I am not an url'}, expected=400)

    def test_short(self):
        j1 = self.api.short.put(
            {'url': 'http://github.com', 'expiry': 3, 'id': 'customid'}
        )
        self.assertTrue(j1['id'] == 'customid')
        self.api.short.put(
            {'url': 'http://github.com', 'id': 'customid'}, expected=400
        )

        j2 = self.api.short.put({'url': 'http://gist.github.com'})

        j = self.api.short.get({'id': 'customid'})
        self.assertTrue(j['url'] == 'http://github.com')

        j = self.api.short.get(data={'id': j2['id']})
        self.assertTrue(j['url'] == 'http://gist.github.com')

        self.api.short.delete({'id': j2['id'], 'secret': j2['secret']})
        self.api.short.get({'id': j2['id']}, expected=404)

        self.api.short.delete({'id': 'customid', 'secret': j1['secret']})
        self.api.short.get({'id': 'customid'}, expected=404)
        j1 = self.api.short.put({'url': 'http://github.com', 'id': 'customid'})
        self.api.short.get({'id': 'customid'})
        self.api.short.delete({'id': 'customid', 'secret': j1['secret']})


class ShortV1TestsRedis(VSTestCase, ShortV1Tests):
    def setUp(self):
        self.app = self.create_app(self.get_redis())
        self.api = APIv1Client(self.app)


class ShortV1TestsSql(VSTestCase, ShortV1Tests):
    def setUp(self):
        self.app = self.create_app(self.get_sql())
        self.api = APIv1Client(self.app)
