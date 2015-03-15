from vs.database.exception import IdAlreadyExists, IdNotFound
from vs.database.base import VSDatabase
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, Integer, DateTime, Boolean
import sqlalchemy.exc
import time


Base = declarative_base()


class Sql(VSDatabase):
    def __init__(self, uri):
        VSDatabase.__init__(self)

        self.engine = create_engine(uri, convert_unicode=True)
        self.session = scoped_session(sessionmaker(bind=self.engine))
        Base.query = self.session.query_property()

    def init_app(self, app):
        VSDatabase.init_app(self, app)

        @app.teardown_request
        def remove_db_session(exception):
            self.session.commit()
            self.session.remove()

    def initialize(self):
        self.create_all()

    def create_all(self):
        Base.metadata.create_all(self.engine)

    def _config_get(self, domain, key):
        c = self.session.query(Config).filter(Config.domain == domain).first()
        if c is None:
            return None
        return getattr(c, key)

    def _config_set(self, domain, key, value):
        c = self.session.query(Config).filter(Config.domain == domain).first()
        if c is None:
            c = Config(domain=domain)
            self.session.add(c)
        setattr(c, key, value)

    def _config_delete(self, domain):
        c = self.session.query(Config).filter(Config.domain == domain).first()
        if c is not None:
            self.session.delete(c)

    def _get(self, domain, id):
        c = self.session.query(ShortURL) \
            .filter(ShortURL.domain == domain) \
            .filter(ShortURL.id == id).first()

        expiry = getattr(c, 'expiry', None)
        if expiry is not None and expiry < time.time():
            self.session.delete(c)
            return None

        return getattr(c, 'url', None)

    def _create(self, domain, id, url, expiry=None):
        if expiry is not None:
            expiry = time.time() + expiry.total_seconds()

        c = ShortURL(id=id, url=url, domain=domain, expiry=expiry)

        try:
            self.session.add(c)
            self.session.flush()
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            raise IdAlreadyExists('Id already exists', 400)

    def _delete(self, domain, id):
        c = self.session.query(ShortURL) \
            .filter(ShortURL.domain == domain) \
            .filter(ShortURL.id == id).first()

        if c is None:
            raise IdNotFound('Id not found', 404)

        self.session.delete(c)


class Config(Base):
    __tablename__ = 'config'

    domain = Column(String(20), primary_key=True)

    default_expiry = Column(Integer)
    max_expiry = Column(Integer)
    custom_ids = Column(Boolean)
    alias = Column(String(20))
    alphabet = Column(String(100))


class ShortURL(Base):
    __tablename__ = 'short_url'

    id = Column(String(50), primary_key=True)
    domain = Column(String(20), primary_key=True)

    url = Column(String(500), nullable=False)
    expiry = Column(Integer)
