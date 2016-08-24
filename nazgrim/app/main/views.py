# -*- coding:utf-8 -*-
__author__ = 'jinxiu.qi'
from . import nazgrim
from . import logger
from ..tools.markdown import markdown
from flask import render_template, send_file, request
from .. import db
import json


@nazgrim.route('/')
def home():
    from ..models import User
    logger.info("%s request /" % request.remote_addr)
    db.create_all()
    text = markdown.to_html('app/article/test.md')
    return render_template('index.html', text=text)


@nazgrim.route('/article')
def article_list():
    logger.info("%s request /article" % request.remote_addr)
    article_list = json.load(open('app/article/articles.json'))
    return render_template('article/list.html', article_list=article_list)


@nazgrim.route('/article/<article_name>')
def article(article_name):
    logger.info("%s request /article/%s" % (request.remote_addr, article_name))
    html = markdown.to_html('app/article/%s/main.md' % article_name)
    return render_template('article/show.html', text=html)


@nazgrim.route('/article/<article_name>/image/<image_name>')
def article_image(article_name, image_name):
    return send_file('article/%s/image/%s' % (article_name, image_name))


@nazgrim.route('/photo')
def photo():
    logger.info("%s request /photo" % request.remote_addr)
    return render_template('photo/list.html')
