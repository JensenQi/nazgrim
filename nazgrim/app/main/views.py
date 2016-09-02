# -*- coding:utf-8 -*-
__author__ = 'jinxiu.qi'
from . import nazgrim
from flask import render_template, send_file, request
from flask.ext.login import login_required
from .. import db
from ..models import Notes
import json
import os

MEDIVH_PATH = os.path.abspath('../medivh')


@nazgrim.route('/')
def home():
    return render_template('index.html')


@nazgrim.route('/new_note', methods=['Post'])
@login_required
def new_note():
    content = request.form.get('content')
    note = Notes(content=content, status=1)
    db.session.add(note)
    db.session.commit()
    return render_template('index.html')


@nazgrim.route('/article')
def article_list():
    path = os.path.join(MEDIVH_PATH, 'list.json')
    article_list = json.load(open(path))
    return render_template('article/list.html', article_list=article_list)


@nazgrim.route('/article/<article_name>/<page_name>')
def get_page(article_name, page_name):
    path = os.path.join(MEDIVH_PATH, article_name, 'html', 'pages', page_name)
    return send_file(path)


@nazgrim.route('/article/<article_name>')
def article(article_name):
    path = os.path.join(MEDIVH_PATH, article_name, 'html', 'main.html')
    with open(path) as fp:
        text = fp.read()
    return render_template('article/show.html', text=text)


@nazgrim.route('/article/<article_name>/image/<image_name>')
def article_image(article_name, image_name):
    return send_file('article/%s/image/%s' % (article_name, image_name))


@nazgrim.route('/photo')
def photo():
    return render_template('photo/list.html')
