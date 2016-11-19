<h1 align="center">python代码highlight测试</h1>
<code class="python">
# -*- coding:utf-8 -*-
__author__ = 'jinxiu.qi'
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __table__name = 'user'
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
</code>