# encoding: utf-8
# encoding: utf-8

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(Form):
    login = StringField(label='Login', validators=[DataRequired(), Length(max=30), Email()])
    password = StringField(label='Password', validators=[DataRequired(), Length(max=60)])


# class RegisterForm(LoginForm):
#     repeat_password = StringField(label='repeat password', validators=[DataRequired(), Length(max=60)])
