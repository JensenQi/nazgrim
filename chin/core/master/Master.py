from TaskMeta import TaskMeta
from TaskDistributor import TaskDistributor
from TaskMonitor import TaskMonitor
from VersionController import VersionController


class Master:
    def __init__(self):
        self.version_controller = VersionController()
        self.task_distributor = TaskDistributor()
        self.task_monitor = TaskMonitor()

    def serve(self):
        self.version_controller.serve()
        self.task_distributor.serve()
        self.task_monitor.serve()

    @staticmethod
    def add_task():
        task = None
        TaskMeta.add(task)

    @staticmethod
    def remove_task():
        task = None
        TaskMeta.remove(task)

    @staticmethod
    def update_task():
        task = None
        TaskMeta.update(task)
        