# encoding: utf-8

from flask import Flask

from config import config
from extensions import extensions_list
from auth import auth_blueprint


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    for ext in extensions_list:
        ext.init_app(app)

    app.register_blueprint(auth_blueprint)

    return app
