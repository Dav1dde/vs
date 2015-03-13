from flask import Blueprint, jsonify, current_app
from flask.ext import restful
import traceback

from vs.database.exception import VSDatabaseException
from vs.views.rest.v1.short import ShortUrl
from vs.views.rest.v1.domain import Domain


rest = Blueprint('rest', __name__)


@rest.errorhandler(VSDatabaseException)
def rest_errorhandler(exc):
    return jsonify(exc.to_dict()), exc.status


@rest.errorhandler(Exception)
def rest_errorhandler(exc):
    ret = {'message': 'Internal Server Error', 'status': 500}
    current_app.logger.exception('Unhandled server error in v1 API')
    if current_app.debug:
        ret['traceback'] = traceback.format_exc()
        ret['type'] = exc.__class__.__name__

    return jsonify(ret), 500


api = restful.Api(rest)
api.add_resource(ShortUrl, '/short')
api.add_resource(Domain, '/domain')
