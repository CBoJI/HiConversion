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

    def test_create_admin_by_managepy(self):
        # test "python manage.py set_admin name password"
        User.set_admin(u'test@test.ru', u'123')
        u = User.query.filter_by(login='test@test.ru').first()
        self.assertTrue(u.admin is True, u)

    def login_as_admin(self):
        response = self.client.post(url_for('auth.login_view'), data={
            'login': self.admin_login,
            'password': self.admin_password,
        }, follow_redirects=True)

    def test_unauthorized_admin_pages(self):
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

    def test_authorized_admin_pages(self):
        # authorize as admin
        response = self.client.post(url_for('auth.login_view'), data={
            'login': self.admin_login,
            'password': self.admin_password,
        }, follow_redirects=True)
        self.assertTrue('You can go to control panel' in response.data)

        # get admin home page
        response = self.client.get(url_for('admin.index'))
        self.assertTrue('Control Panel' in response.data)

    def test_create_invites(self):
        self.login_as_admin()
        # admin creates invite
        response = self.client.post(url_for('admin.index'), data={
            'email': self.invite_email,
        }, follow_redirects=True)
        self.assertTrue('"status": "ok"' in response.data)

    def test_create_invites_with_existed_email(self):
        # cannot create invite if user with email already exists

        # create user
        self.client.get(url_for('auth.invite_view', invite_str=self.invite_str), follow_redirects=True)
        self.client.post(url_for('auth.logout_view'), follow_redirects=True)

        self.login_as_admin()
        # admin creates invite
        response = self.client.post(url_for('admin.index'), data={
            'email': self.invite_email,
        }, follow_redirects=True)
        self.assertTrue("Email already created." in response.data)

    def test_create_bad_invite_with_wrong_email(self):
        self.login_as_admin()
        # admin creates invite with bad args
        response = self.client.post(url_for('admin.index'), data={
            'email': 'bb@bb',
        }, follow_redirects=True)
        self.assertTrue('Invalid email address' in response.data, response.data)

    def test_create_bad_invite_with_not_email(self):
        self.login_as_admin()
        response = self.client.post(url_for('admin.index'), data={
            'email': 'bb',
        }, follow_redirects=True)
        self.assertTrue('Invalid email address' in response.data)

    def test_create_bad_invite_with_missing_email_field(self):
        self.login_as_admin()
        response = self.client.post(url_for('admin.index'), data={
            'not_email': self.invite_email,
            'not_email2': self.invite_email,
        }, follow_redirects=True)
        self.assertTrue('This field is required.' in response.data)

    def test_existing_invites(self):
        # created invite exists
        self.assertTrue(Invite.query.filter_by(email=self.invite_email).first())

        # invite for wrong email not exists
        self.assertFalse(Invite.query.filter_by(email=u'wrong@mail.ru').first())

    def test_post_invite_view_405(self):
        response = self.client.post(url_for('auth.invite_view', invite_str='asfas'), follow_redirects=True)
        self.assertTrue(response.status_code == 405)

    def test_get_invite_view_404(self):
        response = self.client.get(url_for('auth.invite_view', invite_str='asfas'), follow_redirects=True)
        self.assertTrue(response.status_code == 404)

    def test_access_invite_view_with_real_invite(self):
        response = self.client.get(url_for('auth.invite_view', invite_str=self.invite_str), follow_redirects=True)
        self.assertTrue('You can logout' in response.data)

        # cannot access admin pages
        self.assertFalse('You can go to control panel' in response.data)

        u = User.query.filter_by(invite=self.invite_str).first()
        self.assertTrue(u.login == self.invite_email)

    def test_not_reusable_invite(self):
        # invite cannot be accessed twice

        # use invite fot the first time
        self.client.get(url_for('auth.invite_view', invite_str=self.invite_str), follow_redirects=True)

        response = self.client.get(url_for('auth.invite_view', invite_str=self.invite_str), follow_redirects=True)
        self.assertTrue(response.status_code == 404)

    def test_new_user_email(self):
        self.client.get(url_for('auth.invite_view', invite_str=self.invite_str), follow_redirects=True)

        # new users email must be equal to invite email
        u = User.query.filter_by(invite=self.invite_str).first()
        self.assertTrue(u.login == self.invite_email)

    def test_new_user_role(self):
        self.client.get(url_for('auth.invite_view', invite_str=self.invite_str), follow_redirects=True)

        # new user cannot have admin access
        u = User.query.filter_by(invite=self.invite_str).first()
        self.assertTrue(u.admin is False)

    def test_logout_post_405(self):
        # get method now allowed for logout view
        response = self.client.get(url_for('auth.logout_view'), follow_redirects=True)
        self.assertTrue(response.status_code == 405, response.status_code)

        self.login_as_admin()
        response = self.client.post(url_for('auth.logout_view'), follow_redirects=True)
        self.assertTrue('Please sign in' in response.data)

    def test_admin_logout(self):
        self.login_as_admin()
        response = self.client.post(url_for('auth.logout_view'), follow_redirects=True)
        self.assertTrue('Please sign in' in response.data)

    def test_user_logout(self):
        self.client.get(url_for('auth.invite_view', invite_str=self.invite_str), follow_redirects=True)
        response = self.client.post(url_for('auth.logout_view'), follow_redirects=True)
        self.assertTrue('Please sign in' in response.data)