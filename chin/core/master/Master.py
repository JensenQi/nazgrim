# coding=utf-8
from TaskMeta import TaskMeta
from TaskDistributor import TaskDistributor
from TaskMonitor import TaskMonitor
from VersionController import VersionController
from .. import DBSession
import time


class Master:
    def __init__(self):
        self.version_controller = VersionController()
        self.task_distributor = TaskDistributor()
        self.task_monitor = TaskMonitor()

    def serve(self):
        self.version_controller.serve()
        self.task_distributor.serve()
        self.task_monitor.serve()

    def is_live(self):
        return self.version_controller.is_live() and self.task_distributor.is_live() \
               and self.task_monitor.is_live()

    @staticmethod
    def add(task):
        session = DBSession()
        TaskMeta.add(task).by(session)
        session.close()

    @staticmethod
    def remove(task):
        session = DBSession()
        TaskMeta.remove(task).by(session)
        session.close()

    @staticmethod
    def update_task(task):
        session = DBSession()
        TaskMeta.update(task).by(session)
        session.close()
