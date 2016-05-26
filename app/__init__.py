# encoding: utf-8

from flask import Flask

from config import config
from extensions import extensions
from main import main_blueprint


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    for ext in extensions:
        ext.init_app(app)

    app.register_blueprint(main_blueprint)

    return app
