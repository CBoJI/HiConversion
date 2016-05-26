# encoding: utf-8

from datetime import datetime

from flask import render_template, redirect, url_for, Blueprint, request
from flask.ext.login import login_user, logout_user, login_required, current_user
from forms import LoginForm
from models import User

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login_view():
    if current_user.is_authenticated:
        return render_template('logout.html', url='logout')
        # return redirect(url_for('.logout_view'))

    form = LoginForm()
    if form.validate_on_submit():  # valid form passed by POST method
        user = User.query.filter_by(login=form.login.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            user.update(last_login=datetime.now())

            return redirect(url_for('.login_view'))
        else:
            # show error to user
            form.errors.update({'Authentication': ['Invalid username or password.', ]})

    return render_template('login.html', form=form)


@auth.route('/logout', methods=['POST', ])
def logout_view():
    logout_user()
    return redirect(url_for('.login_view'))
