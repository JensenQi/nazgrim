import os

os.chdir('../../../')

import time
from core import DBSession
from core import engine
from core import BaseModel

from unittest import TestCase
from core.master.TaskDistributor import TaskDistributor
from core.master.VersionController import VersionController
from core.master.TaskMeta import TaskMeta
from core.models import Task, TaskQueue
from datetime import datetime


class TestTaskDistributor(TestCase):
    def setUp(self):
        self.count_down = 5
        self.task_distributor = TaskDistributor()
        self.version_controller = VersionController()
        self.session = DBSession()
        BaseModel.metadata.drop_all(engine)
        BaseModel.metadata.create_all(engine)

        task = Task(
                user='root',
                command='shell /home/suit/day_task.sh',
                machine_pool=['slave_1', 'slave_2', 'slave_3'],
                valid=True,
                scheduled_type='day',
                hour=10, minute=11, second=12
        )

        TaskMeta.add(task).by(self.session)
        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_serve(self):
        i = self.count_down
        self.version_controller.serve()
        self.task_distributor.serve()
        while i > 0:
            i -= 1
            print self.version_controller.is_live(), self.task_distributor.is_live()
            time.sleep(1)
