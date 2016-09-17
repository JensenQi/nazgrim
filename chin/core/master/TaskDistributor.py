# coding=utf-8
from threading import Thread
import time
from . import logger
from datetime import datetime
from .. import DBSession
from ..models import Task, TaskQueue
from random import choice


class TaskDistributor:
    def __init__(self):
        self.serve_thread = Thread(target=self._scan)
        self.serve_thread.setDaemon(True)
        self.scan_span = 1

    def _scan(self):
        while True:
            # todo: 扫描逻辑
            midnight = datetime.date(datetime.now()).strftime("%Y%m%d%H%M%S")
            now = datetime.now().strftime("%Y%m%d%H%M%S")
            session = DBSession()

            # 处理未分配机器的
            undistributed_tasks = session.query(TaskQueue) \
                .filter(TaskQueue.version >= midnight) \
                .filter(TaskQueue.version <= now) \
                .filter(TaskQueue.status is None) \
                .all()

            for task in undistributed_tasks:
                task_meta = session.query(Task).filter_by(id=task.task_id).first()
                # todo: 机器负载均衡
                task.execute_machine = choice(task_meta.machine_pool)
                task.pooled_time = datetime.now()
                task.run_count += 1
                task.status = 'waiting'
                session.add(task)

            # 处理放弃/执行失败的
            failed_tasks = session.query(TaskQueue) \
                .filter(TaskQueue.version >= midnight) \
                .filter(TaskQueue.version <= now) \
                .filter((TaskQueue.status == 'abandon') | (TaskQueue.status == 'failed')) \
                .all()

            for task in failed_tasks:
                task_meta = session.query(Task).filter_by(id=task.task_id).fitst()
                if task_meta.rerun is True and task.run_count < task_meta.rerun_count + 1:
                    # todo: 失败机器切换
                    task.execute_machine = choice(task_meta.machine_pool)
                    task.status = 'waiting'
                    task.run_count += 1
                    session.add(task)

            session.commit()
            session.close()
            time.sleep(self.scan_span)

    def serve(self):
        logger.info('Task Distributor 开始服务')
        self.serve_thread.start()

    def is_live(self):
        return self.serve_thread.isAlive()
