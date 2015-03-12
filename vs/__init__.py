from flask import Flask, g


def create_application():
    import vs.config

    app = Flask(__name__)
    app.config.from_object('vs.config')
    app.config['DATABASE'].init_app(app)

    @app.before_request
    def before_request():
        g.database = app.config['DATABASE']

    from vs.views.rest.v1 import rest as rest_v1
    from vs.views.url import url

    app.register_blueprint(rest_v1, url_prefix='/api/v1')
    app.register_blueprint(url)

    return app
