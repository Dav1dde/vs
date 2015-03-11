

class Redis(object):
    def __init__(self, host='localhost', port=6379, db=0):
        pass

    def get(self, id):
        print('get', id)
        return 'http://localhost'

    def create(self, url, expire=None, id=None):
        if expire < 0:
            expire = None

        print('create', url, expire, id)
        return ('idfromcreate', 'secret')

    def delete(self, id, secret):
        print('delete', id, secret)
        return False
