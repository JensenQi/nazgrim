# -*- coding:utf-8 -*-  
__author__ = 'jinxiu.qi'
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import DATABASE_URI, SECRET_KEY
from flask.ext.login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SECRET_KEY'] = SECRET_KEY

    db.init_app(app)
    login_manager.init_app(app)

    from .main import nazgrim
    from .auth import auth
    app.register_blueprint(nazgrim)
    app.register_blueprint(auth, url_prefix='/auth')

    return app


