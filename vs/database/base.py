from vs.database.exception import (
    VSDatabaseException,
    IdNotFound, IdAlreadyExists,
    InvalidDeletionSecret
)

from itsdangerous import Signer, want_bytes
import datetime
import string
import random
import sys


PY2 = sys.version_info[0] == 2
if PY2:
    text_type = unicode
else:
    text_type = str


def want_unicode(s):
    if not isinstance(s, text_type):
        return s.decode('utf-8')
    return s


class NullSigner(object):
    def get_signature(self, id):
        return ''

    def verify_signature(self, id, secret):
        return False


class VSDatabase(object):
    ALLOWED_CHARS = string.ascii_letters + string.digits

    def __init__(self):
        self._s = NullSigner()

    def init_app(self, app):
        secret = app.config['SECRET_KEY']
        if secret:
            self._s = Signer(secret)

    def generate_id(self, alphabet=None):
        if alphabet is None:
            alphabet = self.ALLOWED_CHARS

        length = 3
        id = ''.join(random.sample(alphabet, length))
        while self.has_id(id):
            id = ''.join(random.sample(alphabet, length))
            length = length + 1

        return id

    def get(self, id):
        result = self._get(id)
        if result is None:
            raise IdNotFound('Id "{0}" not found'.format(id))

        return want_unicode(result)

    def has_id(self, id):
        try:
            result = self.get(id)
        except IdNotFound:
            return False

        return result is not None

    def create(self, url, id=None, expire=None):
        if expire is not None:
            expire = datetime.timedelta(days=expire) if expire > 0 else None

        if id is None:
            while True:
                id = self.generate_id()
                try:
                    self._create(id, url, expire)
                except IdAlreadyExists:
                    # race condition, do it again
                    continue
                break
        else:
            # if the key already exists, not our problem
            self._create(id, url, expire)

        return (id, want_unicode(self._s.get_signature(id)))

    def delete(self, id, secret):
        if self._s.verify_signature(want_bytes(id), want_bytes(secret)):
            self._delete(id)
            return True

        raise InvalidDeletionSecret('Invalid secret')

    def _get(self, id):
        raise NotImplementedError

    def _create(self, id, url, expire=None):
        raise NotImplementedError

    def _delete(self, id):
        raise NotImplementedError

