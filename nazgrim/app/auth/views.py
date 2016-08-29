from flask import render_template, request, redirect
from flask.ext.login import login_user
from . import auth

@auth.route('/login', methods=['POST'])
def login():
    user_name = request.form.get('user_name')
    password = request.form.get('password')
    next_url = request.form.get('next')
    return redirect(next_url)
