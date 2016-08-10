# -*- coding:utf-8 -*-  
__author__ = 'jinxiu.qi'
from . import nazgrim
from flask import render_template

@nazgrim.app_errorhandler(404)
def not_found(e):
    return render_template('error.html', error_code='404'), 404


@nazgrim.app_errorhandler(500)
def server_error(e):
    return render_template('error.html', error_code='500'), 500
