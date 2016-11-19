from flask import render_template, request, redirect, flash, url_for
from flask.ext.login import login_user, logout_user, login_required
from . import auth
from ..models import User


@auth.route('/login', methods=['POST'])
def login():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    next_url = request.form.get('next')
    user = User.query.filter_by(name=user_name).first()
    if user is not None and user.verify_password(password):
        login_user(user)
    return redirect(next_url)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    next_url = request.args.get('next')
    return redirect(next_url)
