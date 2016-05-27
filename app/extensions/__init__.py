# encoding: utf-8

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from custom_mail import CustomMail

from app.admin import CustomAdmin

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

mail = CustomMail()
db = SQLAlchemy()
admin = CustomAdmin(db=db)

extensions_list = [login_manager, db, admin, mail, ]
