# -*- coding:utf-8 -*-
__author__ = 'jinxiu.qi'
import markdown2

class MarkDown:
    def __init__(self):
        pass

    @staticmethod
    def to_html(path):
        try:
            html = markdown2.markdown_path(path, extras=["code-friendly"])
        except Exception,e:
            print e
        return html

markdown =  MarkDown()
