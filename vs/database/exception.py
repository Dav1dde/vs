class VSDatabaseException(Exception):
    pass


class IdNotFound(VSDatabaseException):
    pass


class IdAlreadyExists(VSDatabaseException):
    pass


class InvalidDeletionSecret(VSDatabaseException):
    pass
