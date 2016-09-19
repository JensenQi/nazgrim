import os

os.chdir('../../../')

from core import DBSession
from core import engine
from core import BaseModel

from unittest import TestCase
from core.master.VersionController import VersionController
from core.master.TaskDistributor import TaskDistributor
from core.master.TaskMeta import TaskMeta
from core.slave.TaskWorker import TaskWorker
from core.models import Task, TaskQueue
from datetime import datetime
import time


class TestTaskWorker(TestCase):
    def setUp(self):
        self.count_down = 5
        self.task_distributor = TaskDistributor()
        self.version_controller = VersionController()
        self.task_worker = TaskWorker('slave_1')
        self.session = DBSession()
        BaseModel.metadata.drop_all(engine)
        BaseModel.metadata.create_all(engine)
        rerun_task = Task(
                user='root',
                command='python /home/suit/test1.py',
                machine_pool=['slave_1'],
                valid=True,
                rerun=True,
                rerun_times=2,
                scheduled_type='day',
                hour=0, minute=0, second=1
        )
        unrerun_task = Task(
                user='root',
                command='python /home/suit/test.py',
                machine_pool=['slave_1'],
                valid=True,
                scheduled_type='week',
                weekday=datetime.now().isoweekday(),
                hour=0, minute=0, second=2
        )
        TaskMeta.add(rerun_task).by(self.session)
        TaskMeta.add(unrerun_task).by(self.session)
        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_serve(self):
        self.version_controller.serve()
        time.sleep(2)
        self.task_distributor.serve()
        time.sleep(2)
        self.task_worker.serve()
        time.sleep(30)
