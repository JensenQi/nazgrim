# -*- coding:utf-8 -*-  
__author__ = 'jinxiu.qi'
from . import nazgrim
from flask import render_template, request
import traceback

@nazgrim.app_errorhandler(404)
def not_found(e):
    exstr = traceback.format_exc()
    print exstr
    print '请求url', request.url, '失败, 返回404'
    return render_template('error.html', error_code='404'), 404


@nazgrim.app_errorhandler(500)
def server_error(e):
    exstr = traceback.format_exc()
    print exstr
    return render_template('error.html', error_code='500'), 500
