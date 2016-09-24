from . import admin
from flask import render_template


@admin.route('/')
def home():
    return render_template('index.html')

@admin.route('/login')
def login():
    return '<h1>login</h1>'
