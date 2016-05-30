# encoding: utf-8

import random
import string
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declared_attr
from flask_login import UserMixin, AnonymousUserMixin
import inflection

from app.extensions import db, login_manager, mail


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
    # email uses as login
    login = db.Column(db.Unicode(30), unique=True)
    password = db.Column(db.Unicode(60), unique=True)
    invite = db.Column(db.Unicode(36), unique=True)

    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime)

    admin = db.Column(db.BOOLEAN, default=False)

    def __repr__(self):
        return str(self.id)

    def __unicode__(self):
        return self.login

    @staticmethod
    def hash_password(password):
        return unicode(generate_password_hash(password))

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def generate_password(n=8):
        """
        Generate random password of n characters.
        :param n: number of characters.
        """
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

    @staticmethod
    def create_user(email, invite_str):
        password = User.generate_password()
        user = User.create(login=email,
                           password=User.hash_password(password),
                           invite=invite_str,
                           created_at=datetime.now())

        mail.send_login_info(email, password)
        return user

    @staticmethod
    def set_admin(login, password):
        login = unicode(login)
        admin = User.query.filter_by(login=login).first()
        if admin:
            admin.update(password=User.hash_password(password), admin=True)
        else:
            User.create(login=login, password=User.hash_password(password),
                        created_at=datetime.now(), admin=True)


class Invite(UserMixin, CRUDMixin, db.Model):
    invite = db.Column(db.Unicode(36), unique=True)
    email = db.Column(db.Unicode(30), unique=False)  # invite can be sent many times to one email

    created_at = db.Column(db.DateTime, default=datetime.now)
    used = db.Column(db.BOOLEAN, default=False)

    def __repr__(self):
        return str(self.id)

    def __unicode__(self):
        return self.email

    @staticmethod
    def create_invite(email):
        from uuid import uuid4
        invite_str = unicode(uuid4())
        return Invite.create(invite=invite_str, email=email)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
