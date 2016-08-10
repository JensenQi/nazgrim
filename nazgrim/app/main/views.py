# -*- coding:utf-8 -*-
__author__ = 'jinxiu.qi'
from . import nazgrim
from ..tools.markdown import markdown
from flask import render_template, send_file
from .. import db


@nazgrim.route('/')
def home():
    from ..models import User

    db.create_all()
    text = markdown.to_html('app/article/test.md')
    return render_template('index.html', text=text)


@nazgrim.route('/article')
def article_list():
    import json, random

    color = ['#FFB6C1', '#FFC0CB', '#DB7093', '#FF69B4', '#C71585', '#DA70D6', '#556B2F', '#6B8E23', '#008000',
             '#D8BFD8', '#DDA0DD', '#EE82EE', '#8B008B', '#800080', '#BA55D3', '#9400D3', '#9932CC', '#228B22',
             '#4B0082', '#8A2BE2', '#9370DB', '#7B68EE', '#6A5ACD', '#483D8B', '#0000CD', '#696969', '#006400',
             '#191970', '#00008B', '#6495ED', '#B0C4DE', '#778899', '#708090', '#1E90FF', '#4682B4', '#BC8F8F',
             '#87CEFA', '#87CEEB', '#00BFFF', '#ADD8E6', '#B0E0E6', '#5F9EA0', '#AFEEEE', '#FA8072', '#F08080',
             '#00CED1', '#2F4F4F', '#008B8B', '#48D1CC', '#20B2AA', '#40E0D0', '#A9A9A9', '#808080', '#008080',
             '#00FA9A', '#3CB371', '#2E8B57', '#90EE90', '#8FBC8F', '#32CD32', '#B22222', '#800000', '#C0C0C0',
             '#808000', '#BDB76B', '#EEE8AA', '#F0E68C', '#FFD700', '#DAA520', '#FF4500', '#E9967A', '#FF6347',
             '#F5DEB3', '#FFE4B5', '#FFA500', '#FFDEAD', '#D2B48C', '#DEB887', '#CD5C5C', '#A52A2A', '#FF7F50',
             '#FF8C00', '#CD853F', '#FFDAB9', '#F4A460', '#D2691E', '#8B4513', '#A0522D', '#FFA07A', '#000080']
    action = ['metro slide left', 'metro slide right', 'metro slide down', 'metro slide up', 'metro flip horizontal',
              'metro flip vertical']
    article_list = json.load(open('app/article/articles.json'))
    for idx, article in enumerate(article_list):
        article['metro_color'] = random.choice(color)
        article['metro_action'] = random.choice(action)
        article['id'] = idx
    return render_template('article/list.html', article_list=article_list, article_num=len(article_list))


@nazgrim.route('/article/<article_name>')
def article(article_name):
    html = markdown.to_html('app/article/%s/main.md' % article_name)
    return render_template('article/show.html', text=html)


@nazgrim.route('/article/<article_name>/image/<image_name>')
def article_image(article_name, image_name):
    return send_file('article/%s/image/%s' % (article_name, image_name))


@nazgrim.route('/photo')
def photo():
    return render_template('photo/list.html')
