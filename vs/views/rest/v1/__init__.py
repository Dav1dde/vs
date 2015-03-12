from flask import Blueprint
from flask.ext import restful

from vs.views.rest.v1.short import ShortUrl


class MaxExpireException(Exception):
    def __init__(self, val, max_val, msg=None):
        if msg is None:
            msg = 'Expire set to {0}, maximum value is {1}'.format(
                val, max_val
            )

        Exception.__init__(self, msg)

    @classmethod
    def raise_if_required(cls, val, max_val):
        if max_val is not None and max_val > 0 and val > max_val:
            raise cls(val, max_val)


errors = {
    'VSDatabaseException': {
        'message': 'Internal backend error.',
        'status': 500,
    },
    'IdNotFound': {
        'message': 'A short URL with that Id does not exist.',
        'status': 404,
    },
    'IdAlreadyExists': {
        'message': 'Id already exists, chose a different Id.',
        'status': 400
    },
    'InvalidDeletionSecret': {
        'message': 'Invalid secret.',
        'status': 400
    }
}

rest = Blueprint('rest', __name__)
api = restful.Api(rest, errors=errors)

api.add_resource(ShortUrl, '/short')
