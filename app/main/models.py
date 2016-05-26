# encoding: utf-8

from werkzeug.security import generate_password_hash
from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin
import inflection

from app.extensions import db


class CRUDMixin(object):
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def __table_args__(self):
        return {'extend_existing': True}

    @declared_attr
    def __tablename__(self):
        return inflection.pluralize(self.__name__.lower())

    @classmethod
    def get_by_id(cls, id):
        try:
            instance = cls.query.get(int(id))
        except ValueError:
            instance = None
        return instance

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


class User(UserMixin, CRUDMixin, db.Model):
    login = db.Column(db.Unicode(30), unique=True)
    password = db.Column(db.Unicode(60), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
