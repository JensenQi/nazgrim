from . import admin
from flask import render_template


@admin.route('/')
def home():
    return render_template('index.html')


@admin.route('/routine_log')
def routine_log():
    return render_template('routine_log.html')


@admin.route('/login')
def login():
    return '<h1>login</h1>'
