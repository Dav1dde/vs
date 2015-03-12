class VSDatabaseException(Exception):
    pass


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
