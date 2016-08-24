# -*- coding:utf-8 -*-  
__author__ = 'jinxiu.qi'
from flask import Blueprint
nazgrim = Blueprint('nazgrim', __name__)
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s]\t%(asctime)s\t%(message)s',
    datefmt='%y-%m-%d %H:%M:%S',
)
logger = logging.getLogger()

from . import views, errors
