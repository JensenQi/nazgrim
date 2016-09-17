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
    def fields(self, id=Column(Integer, primary_key=True, doc="任务id"),
               user=Column(String(32), doc="任务创建者"),
               group=Column(String(32), doc="任务所属组"),
               create_time=Column(DateTime, doc="任务创建时间"),
               command=Column(Text, doc="任务执行命令"),
               args=Column(Text, doc="任务执行参数"),
               priority=Column(SmallInteger, doc="任务优先级"),
               machine_pool=Column(Json, doc="机器池list"),
               valid=Column(Boolean, index=True, doc="是否调度"),
               rerun=Column(Boolean, index=True, default=False, doc="当失败时是否自动重新执行"),
               rerun_times=Column(SmallInteger, default=0, doc="重新执行次数"),
               scheduled_type=Column(Enum('once', 'day', 'week', 'month', 'year'), index=True, doc="调度频率"),
               year=Column(SmallInteger, doc="调度时间-年"),
               month=Column(SmallInteger, doc="调度时间-月"),
               weekday=Column(SmallInteger, doc="调度时间-周几"),
               day=Column(SmallInteger, doc="调度时间-日"),
               hour=Column(SmallInteger, doc="调度时间-时"),
               minute=Column(SmallInteger, doc="调度时间-分"),
               second=Column(SmallInteger, doc="调度时间-秒")): pass

    # 基础
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, doc="任务id")
    user = Column(String(32), doc="任务创建者")
    group = Column(String(32), doc="任务所属组")
    create_time = Column(DateTime, doc="任务创建时间")

    # 执行相关
    command = Column(Text, doc="任务执行命令")
    args = Column(Text, doc="任务执行参数")
    priority = Column(SmallInteger, default=0, doc="任务优先级")
    machine_pool = Column(Json, doc="机器池list")

    # 调度相关
    valid = Column(Boolean, index=True, default=False, doc="是否调度")
    rerun = Column(Boolean, index=True, default=False, doc="当失败时是否自动重新执行")
    rerun_times = Column(SmallInteger, default=0, doc="重新执行次数")
    scheduled_type = Column(Enum('once', 'day', 'week', 'month', 'year'), index=True, doc="调度频率")
    year = Column(SmallInteger, doc="调度时间-年")
    month = Column(SmallInteger, doc="调度时间-月")
    weekday = Column(SmallInteger, doc="调度时间-周几")
    day = Column(SmallInteger, doc="调度时间-日")
    hour = Column(SmallInteger, doc="调度时间-时")
    minute = Column(SmallInteger, default=0, doc="调度时间-分")
    second = Column(SmallInteger, default=0, doc="调度时间-秒")

    def __repr__(self):
        return '<Task %s>' % self.id


class TaskQueue(BaseModel):
    def fields(
            self, id=Column(Integer, primary_key=True, doc="日志id"),
            task_id=Column(Integer, ForeignKey('task.id'), doc='任务id'),
            version=Column(String(14), doc='版本号'),
            execute_machine=Column(String(32), doc='执行机器'),
            pooled_time=Column(DateTime, doc='入池时间'),
            begin_time=Column(DateTime, doc='开始执行时间'),
            finish_time=Column(DateTime, doc='执行结束时间'),
            status=Column(Enum('waiting', 'abandon', 'running', 'failed', 'killing', 'repairing'), index=True, doc='状态')
    ): pass

    __tablename__ = 'task_queue'

    id = Column(Integer, primary_key=True, doc="日志id")
    task_id = Column(Integer, ForeignKey('task.id'), doc='任务id')
    version = Column(String(14), doc='版本号')
    execute_machine = Column(String(32), doc='执行机器')
    pooled_time = Column(DateTime, doc='入池时间')
    begin_time = Column(DateTime, doc='开始执行时间')
    finish_time = Column(DateTime, doc='执行结束时间')
    status = Column(Enum('waiting', 'abandon', 'running', 'failed', 'killing', 'repairing'), index=True, doc='状态')

    def __repr__(self):
        return '<TaskQueue %s>' % self.id
