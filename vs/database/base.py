from vs.database.exception import (
    VSDatabaseException, IdNotFound, IdAlreadyExists,
    InvalidDeletionSecret, InvalidUrl, InvalidId
)

from flask import request


from itsdangerous import Signer, want_bytes
import datetime
import string
import random
import sys


PY2 = sys.version_info[0] == 2
if PY2:
    from urlparse import urlparse
    text_type = unicode
else:
    from urllib.parse import urlparse
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
    ALLOWED_CHARS = string.ascii_letters + string.digits + '-_'
    MAX_LENGTH = 20

    def __init__(self):
        self._s = NullSigner()
        self._config_defaults = dict()

    def init_app(self, app):
        secret = app.config['SECRET_KEY']
        if secret:
            self._s = Signer(secret)

        self._config_defaults = dict(
            (k.lower(), v) for k, v in app.config['DEFAULTS'].items()
        )

    def generate_id(self, alphabet=None):
        if alphabet is None:
            alphabet = self.ALLOWED_CHARS

        length = 3
        id = ''.join(random.sample(alphabet, length))
        while self.has_id(id):
            id = ''.join(random.sample(alphabet, length))
            length = min(length + 1, self.MAX_LENGTH)

        return id

    def config_get(self, key, domain=None):
        key = key.lower()
        if domain is None:
            domain = urlparse(request.url).netloc
        result = self._config_get(domain, key)
        if result is None:
            result = self._config_defaults.get(key)
        return result

    def config_set(self, key, value, domain=None):
        key = key.lower()
        if domain is None:
            domain = urlparse(request.url).netloc
        self._config_set(domain, key, value)

    def config_delete(self, domain=None):
        if domain is None:
            domain = urlparse(request.url).netloc
        self._config_delete(domain)

    def get_domain(self, domain=None):
        """
        Returns the domain or the alias (if set),
        for the current domain.
        This method requires a flask application-context,
        if called without :param:`domain`.

        :param domain: use this domain instead of the current domain
        """
        if domain is None:
            domain = urlparse(request.url).netloc

        alias = self.config_get('alias', domain=domain)
        if alias is not None:
            domain = alias

        return domain

    def get(self, id):
        domain = self.get_domain()
        result = self._get(domain, id)
        if result is None:
            raise IdNotFound('Id "{0}" not found'.format(id), 404)

        return want_unicode(result)

    def has_id(self, id):
        try:
            result = self.get(id)
        except IdNotFound:
            return False

        return result is not None

    def create(self, url, id=None, expiry=None):
        p = urlparse(url)
        if not p.scheme or not p.netloc:
            raise InvalidUrl('Url does not contain scheme and/or netloc', 400)

        if not self.config_get('custom_ids'):
            id = None

        if expiry is None:
            expiry = self.config_get('default_expiry')

        expiry = min(expiry, self.config_get('max_expiry'))
        if expiry is not None:
            expiry = datetime.timedelta(days=expiry) if expiry > 0 else None

        domain = self.get_domain()

        if id is None:
            while True:
                id = self.generate_id()
                try:
                    self._create(domain, id, url, expiry=expiry)
                except IdAlreadyExists:
                    # race condition, do it again
                    continue
                break
        else:
            if not all(c in self.ALLOWED_CHARS for c in id):
                raise InvalidId('Id contains invalid characters', 400)
            if len(id) > self.MAX_LENGTH:
                raise InvalidId('Id is too long', 400)

            # if the key already exists, not our problem
            self._create(domain, id, url, expiry=expiry)

        return (id, expiry, want_unicode(self._s.get_signature(id)))

    def delete(self, id, secret):
        domain = self.get_domain()

        if self._s.verify_signature(want_bytes(id), want_bytes(secret)):
            self._delete(domain, id)
            return True

        raise InvalidDeletionSecret('Invalid secret', 400)

    def _config_get(self, domain, key):
        raise NotImplementedError

    def _config_set(self, domain, key, value):
        raise NotImplementedError

    def _config_delete(self, domain):
        raise NotImplementedError

    def _get(self, domain, id):
        raise NotImplementedError

    def _create(self, domain, id, url, expiry=None):
        raise NotImplementedError

    def _delete(self, domain, id):
        raise NotImplementedError

