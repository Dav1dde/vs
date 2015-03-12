from vs.database.exception import IdAlreadyExists
from vs.database.base import VSDatabase
import redis


class Redis(VSDatabase):
    def __init__(self, *args, **kwargs):
        VSDatabase.__init__(self)

        self.redis = redis.StrictRedis(*args, **kwargs)

    def _get(self, id):
        return self.redis.get(id)

    def _create(self, id, url, expire=None):
        result = self.redis.set(id, url, ex=expire, nx=True)
        if not result:
            raise IdAlreadyExists('Id already exists')

    def _delete(self, id):
        self.redis.delete(id)
