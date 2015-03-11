from flask import Blueprint, redirect, g


url = Blueprint('url', __name__)


@url.route('/<id>/')
def resolve(id):
    url = g.database.get(id)
    return redirect(url)
