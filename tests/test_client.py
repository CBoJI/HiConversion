from uuid import uuid4
import unittest
from flask import url_for
from app import create_app
from app.extensions import db
from app.auth.models import User, Invite


class FlaskClientTestCase(unittest.TestCase):
    admin_login = u'admin@admin.ru'
    admin_password = u'123'

    invite_str = unicode(uuid4())
    invite_email = u'test@test.ru'

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.generate_db_elements()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def generate_db_elements(self):
        admin = User(login=self.admin_login, password=unicode(User.hash_password(self.admin_password)), admin=True)
        invite = Invite(invite=self.invite_str, email=self.invite_email)
        db.session.add_all([admin, invite])
        db.session.commit()

    def test_login_page(self):
        response = self.client.get(url_for('auth.login_view'))
        self.assertTrue('Please sign in' in response.data)

    def login_as_admin(self):
        response = self.client.post(url_for('auth.login_view'), data={
            'login': self.admin_login,
            'password': self.admin_password,
        }, follow_redirects=True)

    def test_admin_pages(self):
        # unauthorized attempt to get admin main page
        response = self.client.get(url_for('admin.index'), follow_redirects=True)
        self.assertTrue('Please sign in' in response.data)

        # unauthorized attempt to get other admin pages
        admin_pages = ['user', 'invite']
        actions = ['index_view', 'edit_view', 'create_view']
        for page in admin_pages:
            for action in actions:
                # try to list/edit/create
                endpoint = '.'.join([page, action])
                response = self.client.get(url_for(endpoint), follow_redirects=True)
                self.assertTrue('Please sign in' in response.data)

        # authorize as admin
        response = self.client.post(url_for('auth.login_view'), data={
            'login': self.admin_login,
            'password': self.admin_password,
        }, follow_redirects=True)
        self.assertTrue('You can go to control panel' in response.data)

        # get admin home page
        response = self.client.get(url_for('admin.index'))
        self.assertTrue('Control Panel' in response.data)

        # admin creates invite
        response = self.client.post(url_for('admin.index'), data={
            'email': self.invite_email,
        }, follow_redirects=True)
        self.assertTrue('"status": "ok"' in response.data)

        # admin creates invite with bad args
        response = self.client.post(url_for('admin.index'), data={
            'email': 'bb@bb',
        }, follow_redirects=True)
        self.assertTrue('Invalid email address' in response.data, response.data)
        response = self.client.post(url_for('admin.index'), data={
            'email': 'bb',
        }, follow_redirects=True)
        self.assertTrue('Invalid email address' in response.data)
        response = self.client.post(url_for('admin.index'), data={
            'not_email': self.invite_email,
            'not_email2': self.invite_email,
        }, follow_redirects=True)
        self.assertTrue('This field is required.' in response.data)

    def test_invites(self):
        # created invite exists
        self.assertTrue(Invite.query.filter_by(email=self.invite_email).first())
        # invite for wrong email not exists
        self.assertFalse(Invite.query.filter_by(email=u'wrong@mail.ru').first())
