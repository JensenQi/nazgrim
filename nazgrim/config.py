# -*- coding:utf-8 -*-  
__author__ = 'jinxiu.qi'
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read('config/app.ini')
DATABASE_URI = cf.get('db', 'URI')
SECRET_KEY = cf.get('secret', 'key')
