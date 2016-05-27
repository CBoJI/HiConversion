# encoding: utf-8

import os
from datetime import timedelta

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    # Enable/disable the development environment
    DEBUG = False

    # Enable/disable testing mode
    TESTING = False

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    SECRET_KEY = """%> *oO /\ 5LE7/,04@=|[;$G9w%!+)J"""

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # The lifetime of a permanent session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    # Flask-SQLAlchemy will not track modifications of objects and emit signals
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Enable query recording
    SQLALCHEMY_RECORD_QUERIES = False

    # Define the database - we are working with
    # SQLite for this example
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite')
    DATABASE_CONNECT_OPTIONS = {}

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'dev_data.sqlite')


class TestingConfig(BaseConfig):
    # Enable testing mode
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'test_data.sqlite')
    WTF_CSRF_ENABLED = False


class ProductionConfig(BaseConfig):

    @classmethod
    def init_app(cls, app):
        BaseConfig.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import RotatingFileHandler

        error_handler = RotatingFileHandler(
            filename='log')
        error_handler.setLevel(logging.ERROR)
        app.logger.addHandler(error_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
