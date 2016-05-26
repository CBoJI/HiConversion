# encoding: utf-8

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
db = SQLAlchemy()

extensions = [login_manager, db, ]