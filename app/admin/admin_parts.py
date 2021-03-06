# encoding: utf-8

from flask import abort, redirect, url_for, request, jsonify, current_app
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from admin_validators import length_check
from forms import InviteForm


class AccessMIXIN(object):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login_view'))


class AppAdminIndexView(AccessMIXIN, AdminIndexView):
    def __init__(self):
        super(AppAdminIndexView, self).__init__(name=u'Main')

    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = InviteForm()
        if request.method == 'GET':
            return self.render('admin/index.html', form=form)
        else:
            if form.validate():
                from app.extensions import mail
                if mail.send_invite(form.email.data):
                    return jsonify({'status': 'ok'})

            return jsonify(form.errors)


class AdminUser(AccessMIXIN, ModelView):
    column_searchable_list = ('login', )

    form_excluded_columns = ('password', )
    column_exclude_list = ('password', )

    can_create = False

    form_args = dict(
        login=dict(validators=[length_check, ]),
        invite=dict(validators=[length_check, ]),
    )


class AdminInvite(AccessMIXIN, ModelView):
    column_searchable_list = ('email', 'invite', )
    can_create = False

    form_args = dict(
        invite=dict(validators=[length_check, ]),
        email=dict(validators=[length_check, ]),
    )
