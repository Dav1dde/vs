from vs.database.exception import IdAlreadyExists, IdNotFound
from vs.database.base import VSDatabase, want_unicode
import redis
import json


class Redis(VSDatabase):
    def __init__(self, *args, **kwargs):
        VSDatabase.__init__(self)
        self.redis = redis.StrictRedis(*args, **kwargs)

    def _config_get(self, domain, key):
        val = self.redis.hget(domain, key)
        if val is None:
            return None
        return json.loads(want_unicode(val))

    def _config_set(self, domain, key, value):
        value = json.dumps(value)
        self.redis.hset(domain, key, value)

    def _config_delete(self, domain):
        self.redis.delete(domain)

    def _get(self, domain, id):
        key = '{0}#{1}'.format(domain, id)
        return self.redis.get(key)

    def _create(self, domain, id, url, expiry=None):
        key = '{0}#{1}'.format(domain, id)
        result = self.redis.set(key, url, ex=expiry, nx=True)
        if not result:
            raise IdAlreadyExists('Id already exists', 400)

    def _delete(self, domain, id):
        key = '{0}#{1}'.format(domain, id)
        result = self.redis.delete(key)
        if result == 0:
            raise IdNotFound('Id not found', 404)

