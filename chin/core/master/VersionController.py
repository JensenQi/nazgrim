# coding=utf-8
from ..models import Task, TaskQueue
from datetime import datetime
import time
from threading import Thread
from . import logger
from .. import DBSession


class VersionController:
    def __init__(self):
        self.scan_span = 2

    def _scan(self):
        while self.is_serving:
            cur_date = datetime.date(datetime.now())
            if self.date != cur_date:
                self.date = cur_date
                self.init()
            print cur_date
            time.sleep(self.scan_span)

    def _start(self):
        self.date = None
        self.is_serving = True
        self.serve_thread = Thread(target=self._scan)
        logger.info('Version Controller 开始服务')
        self.serve_thread.start()

    def _stop(self):
        self.is_serving = False
        logger.info('Version Controller 服务正在关闭...')
        time.sleep(self.scan_span * 2)
        if self.serve_thread.isAlive():
            info = "Version Controller在is_serving置False后两个扫描周期没没有关闭"
            logger.error(info)
            raise Exception(info)
        else:
            logger.info('Version Controller 服务已关闭')

    def _restart(self):
        logger.info('Version Controller 服务重启...')
        self._stop()
        self._start()

    def serve(self, action='start'):
        if action == 'start':
            self._start()
        elif action == 'stop':
            self._stop()
        elif action == 'restart':
            self._restart()
        else:
            info = 'Version Controller只支持start/stop/restart, 不支持%s操作' % action
            logger.error(info)
            raise Exception(info)

    def init(self):

        def append_queue(sess, task_id, task_version):
            queue = session.query(TaskQueue).filter_by(task_id=task_id, version=task_version).all()
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
                if task.day == self.date.day():
                    append_queue(session, task.id, version)
            elif task.scheduled_type == 'year':
                if task.day == self.date.day() and task.month == self.date.month():
                    append_queue(session, task.id, version)
            elif task.scheduled_type == 'once':
                if datetime(task.day, task.month, task.day) == self.date:
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
