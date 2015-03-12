from flask import Blueprint
from flask.ext import restful

from vs.views.rest.v1.short import ShortUrl


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
    },
    'InvalidId': {
        'message': 'Id contains invalid characters.',
        'status': 400
    },
    'InvalidUrl': {
        'message': 'Url does not contain scheme and/or netloc.',
        'status': 400
    }
}

rest = Blueprint('rest', __name__)
api = restful.Api(rest, errors=errors)

api.add_resource(ShortUrl, '/short')
