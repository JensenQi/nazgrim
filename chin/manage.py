# -*- coding:utf-8 -*-  
__author__ = 'jinxiu.qi'
from flask.ext.script import Manager, Shell, Server
from admin import create_app
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = create_app()

manager = Manager(app)
server = Server(host="127.0.0.1", port=4546)
manager.add_command("runserver", server)

if __name__ == '__main__':
    manager.run()
