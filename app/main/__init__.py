# -*- coding:utf-8 -*-  
__author__ = 'jinxiu.qi'
from flask import Blueprint
nazgrim = Blueprint('nazgrim', __name__)

from . import views, errors
