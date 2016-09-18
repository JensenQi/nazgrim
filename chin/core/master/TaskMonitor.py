# coding=utf-8
from ..models import TaskQueue
from threading import Thread
import time
from . import logger


class TaskMonitor:
    def __init__(self):
        self.serve_thread = Thread(target=self._scan)
        self.serve_thread.setDaemon(True)
        self.scan_span = 2

    def _scan(self):
        while True:
            # todo: 扫描逻辑
            time.sleep(self.scan_span)

    def serve(self):
        logger.info('Task Monitor 开始服务')
        self.serve_thread.start()

    def is_live(self):
        return self.serve_thread.isAlive()

    @staticmethod
    def handle_timeout():
        pass

    @staticmethod
    def handle_failed():
        pass

    @staticmethod
    def kill(task):
        pass
