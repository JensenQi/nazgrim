# coding=utf-8
from ..models import Task, TaskQueue
from datetime import datetime
import time
from threading import Thread
from . import logger
from .. import DBSession


class VersionController:
    def __init__(self):
        self.date = None
        self.serve_thread = Thread(target=self._scan)
        self.serve_thread.setDaemon(True)
        self.scan_span = 2

    def _scan(self):
        while True:
            cur_date = datetime.date(datetime.now())
            if self.date != cur_date:
                self.date = cur_date
                self.init()
            print cur_date
            time.sleep(self.scan_span)

    def serve(self):
        logger.info('Version Controller 开始服务')
        self.serve_thread.start()

    def is_live(self):
        return self.serve_thread.isAlive()

    def init(self):
        def append_queue(sess, task_id, task_version):
            item_is_not_exist = session.query(TaskQueue).filter_by(task_id=task_id, version=task_version).all() == []
            if item_is_not_exist:
                sess.add(TaskQueue(task_id=task_id, version=task_version))

        session = DBSession()
        valid_tasks = session.query(Task).filter_by(valid=True).all()
        for task in valid_tasks:
            version = datetime(self.date.year, self.date.month, self.date.day, task.hour, task.minute,
                               task.second).strftime('%Y%m%d%H%M%S')
            if task.scheduled_type == 'day':
                append_queue(session, task.id, version)
            elif task.scheduled_type == 'week':
                if task.weekday == self.date.isoweekday():
                    append_queue(session, task.id, version)
            elif task.scheduled_type == 'month':
                if task.day == self.date.day:
                    append_queue(session, task.id, version)
            elif task.scheduled_type == 'year':
                if task.day == self.date.day and task.month == self.date.month:
                    append_queue(session, task.id, version)
            elif task.scheduled_type == 'once':
                if datetime(task.year, task.month, task.day).date() == self.date:
                    append_queue(session, task.id, version)
            else:
                session.commit()
                session.close()
                raise Exception('不支持的调度周期%s' % task.scheduled_type)
        session.commit()
        session.close()

    @staticmethod
    def handle_add(task, session):
        pass

    @staticmethod
    def handle_remove(task, session):
        pass

    @staticmethod
    def handle_update(task, session):
        pass
