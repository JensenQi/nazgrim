# -*- coding:utf-8 -*-
__author__ = 'jinxiu.qi'
from . import nazgrim
from flask import render_template, send_file, request, redirect
from flask.ext.login import login_required
from .. import db
from ..models import Notes
import json
import os
from datetime import datetime
import math

MEDIVH_PATH = os.path.abspath('../medivh')


@nazgrim.route('/')
def home():
    page = request.args.get('page', default=1, type=int)
    page_size = 10
    notes = Notes.query\
        .filter_by(status=1)\
        .order_by(Notes.id.desc())\
        .paginate(page, page_size, error_out=False)\
        .items
    max_page = int(math.ceil(1.0 * Notes.query.filter_by(status=1).count() / page_size))
    return render_template('index.html', notes=notes, page=page, max_page=max_page)


@nazgrim.route('/new_note', methods=['Post'])
@login_required
def new_note():
    content = request.form.get('content')
    note = Notes(content=content, status=1, create_time=datetime.now())
    db.session.add(note)
    db.session.commit()
    return redirect('/')


@nazgrim.route('/delete_note', methods=['Get'])
@login_required
def delete_note():
    note = Notes.query.filter_by(id=request.args.get('id')).first()
    note.status = 0
    db.session.commit()
    return redirect('/')


@nazgrim.route('/article')
def article_list():
    path = os.path.join(MEDIVH_PATH, 'list.json')
    article_list = json.load(open(path))
    return render_template('article/list.html', article_list=article_list)


@nazgrim.route('/article/<article_name>')
def article(article_name):
    path = os.path.join(MEDIVH_PATH, article_name, 'html', 'main.html')
    with open(path) as fp:
        text = fp.read()
    return render_template('article/show.html', text=text)


@nazgrim.route('/article/<article_name>/<page_name>')
def get_page(article_name, page_name):
    path = os.path.join(MEDIVH_PATH, article_name, 'html', 'pages', page_name)
    return send_file(path)


@nazgrim.route('/photo')
def photo():
    return render_template('photo/list.html')


@nazgrim.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico')
