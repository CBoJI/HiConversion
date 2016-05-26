# encoding: utf-8

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin, AnonymousUserMixin
import inflection

from app.extensions import db, login_manager


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

    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime)

    admin = db.Column(db.BOOLEAN, default=False)

    def __repr__(self):
        return str(self.id)

    def __unicode__(self):
        return self.login

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def set_admin(login, password):
        admin = User.query.filter_by(login=login).first()
        if admin:
            admin.update(password=User.hash_password(password), admin=True)
        else:
            User.create(login=login, password=User.hash_password(password),
                        created_at=datetime.now(), admin=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
