# -*- coding:utf-8 -*-
__author__ = 'jinxiu.qi'
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password 只有写权限')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'user', self.id, self.name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    status = db.Column(db.SmallInteger, index=True)
    create_time = db.Column(db.DateTime, default=datetime.now())
