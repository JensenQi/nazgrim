# -*- coding:utf-8 -*-  
__author__ = 'jinxiu.qi'
from . import nazgrim, logger
from flask import render_template, request

@nazgrim.app_errorhandler(404)
def not_found(e):
    logger.error('%s request %s <404> : %s' % (request.remote_addr, request.url, e))
    return render_template('error.html', error_code='404'), 404


@nazgrim.app_errorhandler(500)
def server_error(e):
    logger.error('%s request %s <500> : %s' % (request.remote_addr, request.url, e))
    return render_template('error.html', error_code='500'), 500
