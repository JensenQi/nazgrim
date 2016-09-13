import os

os.chdir('../../../')

from unittest import TestCase
from core.master.TaskMeta import TaskMeta
from core.models import Task
from datetime import datetime
from core import DBSession


class TestTaskMeta(TestCase):
    def setUp(self):
        self.python_task = Task(
                user='jinxiu.qi',
                group=None,
                create_time=datetime.now(),
                command='python /home/suit/test.py',
                machine_pool=['dw1', 'dw2', 'dw3'],
                valid=True,
                scheduled_type='day',
                hour=10,
                minute=0,
                second=0,
                priority=10,
        )
        self.shell_task = Task(
                user='root',
                group=None,
                create_time=datetime.now(),
                command='shell /home/suit/test.sh',
                machine_pool=['data1', 'data2', 'data3'],
                valid=True,
                scheduled_type='week',
                hour=10,
                minute=0,
                second=0,
                priority=10,
        )
        self.session = DBSession()

    def tearDown(self):
        self.session.close()

    def test_add(self):
        self.assertTrue(self.python_task.id is None)
        TaskMeta.add(self.python_task, self.session)
        self.assertTrue(self.python_task.id is not None)

        self.assertTrue(self.shell_task.id is None)
        TaskMeta.add(self.shell_task, self.session)
        self.assertTrue(self.shell_task.id is not None)

        self.assertEqual(self.python_task.id + 1, self.shell_task.id)

    def test_remove(self):
        valid_count_pre = self.session.query(Task).filter_by(valid=True).count()
        TaskMeta.add(self.python_task, self.session)
        valid_count_mid = self.session.query(Task).filter_by(valid=True).count()
        TaskMeta.remove(self.python_task, self.session)
        valid_count_post = self.session.query(Task).filter_by(valid=True).count()

        self.assertEqual(valid_count_pre + 1, valid_count_mid)
        self.assertEqual(valid_count_mid - 1, valid_count_post)
        self.assertEqual(valid_count_pre, valid_count_post)


