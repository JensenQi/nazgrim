# -*- coding:utf-8 -*-  
__author__ = 'jinxiu.qi'
from flask.ext.script import Manager, Shell
from app import create_app

app = create_app()

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
