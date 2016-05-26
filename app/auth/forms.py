# encoding: utf-8

from flask_wtf import Form
from wtforms import StringField, validators
from wtforms.validators import DataRequired, Email, Length

from models import User


class LoginForm(Form):
    login = StringField(label='Login', validators=[DataRequired(), Length(max=30), Email()])
    password = StringField(label='Password', validators=[DataRequired(), Length(max=60)])


class ConsoleRegisterForm(LoginForm):

    def validate_login(self, field):
        user = User.query.filter_by(login=self.login.data).first()
        if user is not None:
            raise validators.ValidationError('User already exists.')

    def validate_csrf_token(self, field):
        """Disable csrf validation for possibility to use this form from console by manage.py"""
        pass
