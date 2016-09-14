# coding=utf-8
from config import DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import BaseModel

engine = create_engine(DATABASE_URI)
DBSession = sessionmaker(engine)

from master.Master import Master


def run(role):
    BaseModel.metadata.create_all(engine)
    if role is 'master':
        master = Master()
        master.serve()
    elif role is 'slave':
        # todo: 启动slave
        print 'slave'
    else:
        print '只支持master和slave参数'
