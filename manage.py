# encoding: utf-8

import os

from flask.ext.script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.extensions import db
from app import create_app
from app.main.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def set_admin(password):
    """
    Creates new user (login=admin) or updates its password
    """

    try:
        User.set_admin(password)
    except Exception, e:
        print e

if __name__ == '__main__':
    manager.run()
