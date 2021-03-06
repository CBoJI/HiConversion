# encoding: utf-8

from flask_wtf import Form
from wtforms import StringField, validators
from wtforms.validators import DataRequired, Email, Length


class InviteForm(Form):
    email = StringField(label='Email', validators=[DataRequired(), Length(max=30), Email()])

    def validate_email(self, field):
        from app.auth.models import User
        if User.query.filter_by(login=self.email.data).first():
            raise validators.ValidationError('Email already created.')
