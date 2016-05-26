# encoding: utf-8

from flask import abort, redirect, url_for, request, jsonify
from flask_login import current_user
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

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
                return jsonify({'status': 'ok'})
            else:
                return jsonify(form.errors)


class AdminUser(AccessMIXIN, ModelView):
    column_searchable_list = ('login', )

    form_excluded_columns = ('password', )
    column_exclude_list = ('password', )

    can_create = False
