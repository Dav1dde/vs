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

    def test_domain(self):
        self.api.short.put({'url': 'http://github.com', 'id': 'works'})
        j = self.api.short.get({'id': 'works'})
        self.assertTrue(j['url'] == 'http://github.com')

        self.api.domain.put(
            {'api_key': 'API_KEY', 'default_expiry': 13}, expected=200
        )

        self.api.domain.put(
            {'api_key': 'API_KEY', 'max_expiry': 15,
             'custom_ids': False, 'alias': 'notthisdomain'}, expected=200
        )

        j = self.api.domain.get({'api_key': 'API_KEY'})
        self.assertTrue(j['default_expiry'] == 13)
        self.assertTrue(j['max_expiry'] == 15)
        self.assertTrue(j['custom_ids'] == False)
        self.assertTrue(j['alias'] == 'notthisdomain')

        self.api.short.put({'url': 'http://github.com'})
        self.api.short.put({'url': 'http://github.com', 'id': 'broken'}, 400)
        self.api.short.get({'id': 'works'}, 404)

        self.api.domain.delete({'api_key': 'API_KEY'})

        defaults = self.app.config['DEFAULTS']
        j = self.api.domain.get({'api_key': 'API_KEY'})
        self.assertTrue(j['default_expiry'] == defaults['default_expiry'])
        self.assertTrue(j['max_expiry'] == defaults['max_expiry'])
        self.assertTrue(j['custom_ids'] == defaults['custom_ids'])
        self.assertTrue(j['alias'] == defaults['alias'])

        j = self.api.short.get({'id': 'works'})
        self.assertTrue(j['url'] == 'http://github.com')

    def test_api_key(self):
        self.api.domain.get({'api_key': 'ThisIsWrong'}, expected=403)
        self.api.domain.put({'api_key': 'ThisIsWrong'}, expected=403)
        self.api.domain.delete({'api_key': 'ThisIsWrong'}, expected=403)

        self.api.domain.get({'api_key': 'API_KEY'}, expected=200)
        self.api.domain.put({'api_key': 'API_KEY'}, expected=200)
        self.api.domain.delete({'api_key': 'API_KEY'}, expected=200)
