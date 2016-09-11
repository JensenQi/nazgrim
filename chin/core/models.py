# coding=utf-8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, Boolean, Time, String, DateTime, SmallInteger, ForeignKey

BaseModel = declarative_base()


class Task(BaseModel):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    command = Column(Text)
    args = Column(Text)
    valid = Column(Boolean, index=True)
    scheduled_time = Column(Time)
    # todo: 优先级
    # todo: 机器池
    # todo: 创建者


class ExcLog(BaseModel):
    __tablename__ = 'exc_logs'
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    version = Column(String(14))
    pooled_time = Column(DateTime)
    begin_time = Column(DateTime)
    finish_time = Column(DateTime)
    status = Column(SmallInteger, index=True)
