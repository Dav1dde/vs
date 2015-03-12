from flask import Blueprint, redirect, g, abort

from vs.database.exception import IdNotFound


url = Blueprint('url', __name__)


@url.route('/<id>')
def resolve(id):
    try:
        url = g.database.get(id)
    except IdNotFound:
        return abort(404)

    return redirect(url)
