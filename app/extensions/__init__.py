# encoding: utf-8

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from mail import CustomMail

from app.admin import CustomAdmin

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
custom_mail = CustomMail()

db = SQLAlchemy()
custom_admin = CustomAdmin(db=db)

extensions_list = [login_manager, db, custom_admin, custom_mail, ]
