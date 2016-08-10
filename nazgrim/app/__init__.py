# -*- coding:utf-8 -*-  
__author__ = 'jinxiu.qi'
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import DATABASE_URI

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    db.init_app(app)

    from .main import nazgrim
    app.register_blueprint(nazgrim)

    return app


