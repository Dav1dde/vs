from flask import Flask, g


def create_application():
    import vs.config

    app = Flask(__name__)
    app.config.from_object('vs.config')
    app.config['DATABASE'].init_app(app)

    @app.before_request
    def before_request():
        g.database = app.config['DATABASE']

    from vs.views.rest import rest
    from vs.views.url import url

    app.register_blueprint(rest, url_prefix='/api')
    app.register_blueprint(url)

    return app
