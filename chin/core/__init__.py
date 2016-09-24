# coding=utf-8
from config import DATABASE_URI, MACHINE_NAME
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import BaseModel

engine = create_engine(DATABASE_URI)
DBSession = sessionmaker(engine)

from master.Master import Master
from slave.TaskWorker import TaskWorker


def run(role):
    BaseModel.metadata.create_all(engine)
    if role is 'master':
        master = Master()
        master.serve()
    elif role is 'slave':
        worker = TaskWorker(MACHINE_NAME)
        worker.serve()
    else:
        print '只支持master和slave参数'
