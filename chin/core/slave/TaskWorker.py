# coding=utf-8
from . import logger
from threading import Thread
import time
from ..models import Task, TaskQueue
from .. import DBSession
from datetime import datetime
from subprocess import Popen
from ..master.TaskMonitor import TaskMonitor


class Shell:
    def __init__(self, command, task_id, version):
        self.command = command
        self.task_id = task_id
        self.version = version
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        self.log = open('{}_{}_{}.log'.format(self.task_id, self.version, now), 'w')

    def run(self):
        self._process = Popen(self.command, shell=True, stdout=self.log, stderr=self.log)

    def is_running(self):
        return self._process.poll() is None

    def kill(self):
        self._process.kill()

    def return_code(self):
        return self._process.returncode


class TaskWorker:
    def __init__(self):
        self.serve_thread = Thread(target=self._scan)
        self.serve_thread.setDaemon(True)
        self.scan_span = 2
        self.name = None
        self.running_tasks = []

    def _scan(self):
        while True:
            session = DBSession()

            # 启动新任务
            todo_tasks = session.query(TaskQueue).filter_by(execute_machine=self.name, status='waiting').all()
            for task in todo_tasks:
                # todo: 主动放弃 ＆ 资源抢占
                task_meta = session.query(Task).filter_by(id=task.task_id).first()
                command = '{} {}'.format(task_meta.command, task_meta.args)
                shell = Shell(command, task.task_id, task.version)
                shell.run()
                self.running_tasks.append(shell)
                task.status = 'running'
                task.begin_time = datetime.now()
                session.add(task)

            # 执行完毕的任务处理逻辑
            for shell in self.running_tasks:
                if not shell.is_running():
                    self.running_tasks.remove(shell)
                    task = session.query(TaskQueue).filter_by(task_id=shell.task_id, version=shell.version).first()
                    task.finish_time = datetime.now()
                    if shell.return_code() != 0:
                        task.status = 'failed'
                        TaskMonitor.handle_failed(shell.task_id, shell.version)
                    else:
                        task.status = 'finish'
                    session.add(task)

            # 杀死任务的处理逻辑
            kill_tasks = session.query(TaskQueue).filter_by(status='killing').all()
            for shell in self.running_tasks:
                for task in kill_tasks:
                    if shell.task_id == task.task_id and shell.version == task.version:
                        shell.kill()
                        task.status = 'failed'
                        task.finish_time = datetime.now()
                        TaskMonitor.handle_failed(shell.task_id, shell.version)
                        session.add(task)

            session.commit()
            time.sleep(self.scan_span)

    def serve(self):
        logger.info('Task Worker 开始服务')
        self.serve_thread.start()

    def is_live(self):
        return self.serve_thread.isAlive()

