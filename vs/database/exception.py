class VSDatabaseException(Exception):
    def __init__(self, message, status=500, **kwargs):
        Exception.__init__(self, message)

        self.message = message
        self.status = status
        self.kwargs = kwargs

    def to_dict(self):
        ret = {
            'message': self.message,
            'status': self.status,
            'type': self.__class__.__name__
        }
        ret.update(self.kwargs)
        return ret


class InvalidId(VSDatabaseException):
    pass


class InvalidUrl(VSDatabaseException):
    pass


class IdNotFound(VSDatabaseException):
    pass


class IdAlreadyExists(VSDatabaseException):
    pass


class InvalidDeletionSecret(VSDatabaseException):
    pass
