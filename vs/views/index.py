from flask import (
    Blueprint, redirect, g, abort,
    render_template, current_app
)

from vs.database.exception import IdNotFound


index = Blueprint('index', __name__)


@index.route('/')
def landing():
    if current_app.config['ENABLE_FRONTEND']:
        return render_template('index.html')
    return abort(404)


@index.route('/<id>')
def url(id):
    try:
        url = g.database.get(id)
    except IdNotFound:
        return abort(404)

    return redirect(url)

