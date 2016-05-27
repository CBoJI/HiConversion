# encoding: utf-8

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import admin_parts as ap


class CustomAdmin(Admin):

    def __init__(self, db, **kwargs):
        self.db = db
        kwargs.update({
            'name': 'Control Panel',
            'index_view': ap.AppAdminIndexView(),
            'template_mode': 'bootstrap3'
        })
        super(self.__class__, self).__init__(**kwargs)

        from app.auth.models import User, Invite
        self.add_view(ap.AdminUser(User, self.db.session))
        self.add_view(ap.AdminInvite(Invite, self.db.session))
