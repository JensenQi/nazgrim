# coding=utf-8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, Boolean, String, DateTime, SmallInteger, ForeignKey, Enum, TypeDecorator
import enum, json

BaseModel = declarative_base()


class Json(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)


class Task(BaseModel):
    # 基础
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, doc="任务id")
    user = Column(String(32), doc="任务创建者")
    group = Column(String(32), doc="任务所属组")
    create_time = Column(DateTime, doc="任务创建时间")

    # 执行相关
    command = Column(Text, doc="任务执行命令")
    args = Column(Text, doc="任务执行参数")
    priority = Column(SmallInteger, doc="任务优先级")
    machine_pool = Column(Json, doc="机器池list")

    # 调度相关
    valid = Column(Boolean, index=True, doc="是否调度")
    scheduled_type = Column(Enum('once', 'day', 'week', 'month', 'year'), index=True, doc="调度频率")
    year = Column(SmallInteger, doc="调度时间-年")
    month = Column(SmallInteger, doc="调度时间-月")
    day = Column(SmallInteger, doc="调度时间-日")
    hour = Column(SmallInteger, doc="调度时间-时")
    minute = Column(SmallInteger, doc="调度时间-分")
    second = Column(SmallInteger, doc="调度时间-秒")


class TaskQueue(BaseModel):
    __tablename__ = 'task_queue'
    id = Column(Integer, primary_key=True, doc="日志id")
    task_id = Column(Integer, ForeignKey('task.id'), doc='任务id')
    version = Column(String(14), doc='版本号')
    pooled_time = Column(DateTime, doc='入池时间')
    begin_time = Column(DateTime, doc='开始执行时间')
    finish_time = Column(DateTime, doc='执行结束时间')
    status = Column(Enum('waiting', 'running', 'failed', 'killing', 'repairing'), index=True, doc='状态')
