# -*- coding:utf-8 -*-  
__author__ = 'jinxiu.qi'
from flask.ext.script import Manager, Shell
from app import create_app
import logging
import sys, os

app = create_app()

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s]\t%(message)s',
    datefmt='%y-%m-%d %H:%M:%S',
    stream=sys.stdout
)

app.logger.addHandler(logging.getLogger())

manager = Manager(app)


if __name__ == '__main__':
    manager.run()
