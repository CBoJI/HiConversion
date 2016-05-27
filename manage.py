# encoding: utf-8

import os

import coverage
from flask.ext.script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.extensions import db
from app import create_app
from app.auth.models import User
from app.auth.forms import ConsoleRegisterForm

COV = coverage.coverage(branch=True, include='app/*')
COV.start()

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def set_admin(login, password):
    """
    Creates new user (login=<email>) or updates its password
    """

    form = ConsoleRegisterForm(login=login, password=password)
    if form.validate():
        try:
            User.set_admin(login, password)
            print 'Admin-user created (%s)' % login
        except Exception, e:
            print e
    else:
        print form.errors


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


if __name__ == '__main__':
    manager.run()
