# encoding: utf-8

from flask import render_template, redirect, url_for, Blueprint

from forms import LoginForm
from models import User

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index_view():
    form = LoginForm()
    if form.validate_on_submit():  # valid form passed by POST method

        User.create(login=form.login.data, password=User.hash_password(form.password.data))

        return redirect(url_for('.logout_view'))

    return render_template('login.html', form=form)


@main.route('/logout')
def logout_view():
    return render_template('logout.html')
