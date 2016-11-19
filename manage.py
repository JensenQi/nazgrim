# -*- coding:utf-8 -*-  
__author__ = 'jinxiu.qi'
from flask.ext.script import Manager, Shell
from app import create_app
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = create_app()

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
