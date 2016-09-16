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
        while True:
            print time.time(),self.version_controller.is_live()
            time.sleep(1)

    @staticmethod
    def add_task():
        task = None
        session = DBSession()
        TaskMeta.add(task, session)
        session.close()

    @staticmethod
    def remove_task():
        task = None
        session = DBSession()
        TaskMeta.remove(task, session)
        session.close()

    @staticmethod
    def update_task():
        task = None
        session = DBSession()
        TaskMeta.update(task, session)
        session.close()

        