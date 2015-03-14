from unittest import TestCase

import vs.database
from vs import create_application


class VSTestCase(TestCase):
    def create_app(self, db):
        app = create_application()
        app.config.from_object('test.vs_config')
        app.config['DATABASE'] = db
        app.config['DATABASE'].init_app(app)
        app.debug = True

        return app

    def get_sql(self):
        db = vs.database.Sql('sqlite://')
        db.create_all()
        return db

    def get_redis(self):
        return vs.database.Redis(
            host='localhost', port=4999, db=0
        )
