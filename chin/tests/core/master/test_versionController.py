import os

os.chdir('../../../')

import time
from core import DBSession
from core import engine
from core import BaseModel

from unittest import TestCase
from core.master.VersionController import VersionController
from core.master.TaskMeta import TaskMeta
from core.models import Task, TaskQueue
from datetime import datetime


class TestVersionController(TestCase):
    def setUp(self):
        self.version_controller = VersionController()
        self.session = DBSession()
        BaseModel.metadata.drop_all(engine)
        BaseModel.metadata.create_all(engine)

        day_task = Task(
                user='root',
                command='shell /home/suit/day_task.sh',
                valid=True,
                scheduled_type='day',
                hour=10, minute=11, second=12
        )

        week_task_run_today = Task(
                user='root',
                command='shell /home/suit/week_task_run_today.sh',
                valid=True,
                scheduled_type='week',
                weekday=datetime.today().isoweekday(), hour=1, minute=1, second=2
        )

        week_task_not_run_today = Task(
                user='root',
                command='shell /home/suit/week_task_not_run_today.sh',
                valid=True,
                scheduled_type='week',
                weekday=datetime.today().isoweekday() + 2, hour=1, minute=4, second=7
        )

        month_task_run_today = Task(
                user='root',
                command='shell /home/suit/month_task_run_today.sh',
                valid=True,
                scheduled_type='month',
                day=datetime.today().day, hour=5, minute=42, second=23
        )

        month_task_not_run_today = Task(
                user='root',
                command='shell /home/suit/month_task_not_run_today.sh',
                valid=True,
                scheduled_type='month',
                day=datetime.today().day + 1, hour=5, minute=42, second=23
        )

        year_task_run_today = Task(
                user='root',
                command='shell /home/suit/year_task_run_today.sh',
                valid=True,
                scheduled_type='year',
                month=datetime.today().month, day=datetime.today().day, hour=17, minute=30, second=15
        )

        year_task_not_run_today = Task(
                user='root',
                command='shell /home/suit/year_task_not_run_today.sh',
                valid=True,
                scheduled_type='year',
                month=datetime.today().month, day=datetime.today().day + 1, hour=19, minute=32, second=0
        )

        once_task_run_today = Task(
                user='root',
                command='shell /home/suit/once_task_run_today.sh',
                valid=True,
                scheduled_type='once',
                year=datetime.today().year, month=datetime.today().month, day=datetime.today().day, hour=21, minute=45,
                second=0
        )

        once_task_not_run_today = Task(
                user='root',
                command='shell /home/suit/once_task_not_run_today.sh',
                valid=True,
                scheduled_type='once',
                year=datetime.today().year, month=datetime.today().month, day=datetime.today().day + 1, hour=21,
                minute=50, second=0
        )

        invalid_task = Task(
                user='root',
                command='shell /home/suit/invalid_task.sh',
                valid=False,
                scheduled_type='once',
                year=datetime.today().year, month=datetime.today().month, day=datetime.today().day + 1, hour=21,
                minute=50, second=0
        )

        TaskMeta.add(day_task).by(self.session)
        TaskMeta.add(week_task_run_today).by(self.session)
        TaskMeta.add(week_task_not_run_today).by(self.session)
        TaskMeta.add(month_task_run_today).by(self.session)
        TaskMeta.add(month_task_not_run_today).by(self.session)
        TaskMeta.add(year_task_run_today).by(self.session)
        TaskMeta.add(year_task_not_run_today).by(self.session)
        TaskMeta.add(once_task_run_today).by(self.session)
        TaskMeta.add(once_task_not_run_today).by(self.session)
        TaskMeta.add(invalid_task).by(self.session)

        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_serve(self):
        self.version_controller.serve()
        count_down = 2
        while count_down > 0:
            time.sleep(1)
            count_down -= 1

        self.assertEqual(
            self.session.query(TaskQueue).filter_by(task_id=1).first().version,
            datetime.today().strftime('%Y%m%d')+'101112'
        )

        self.assertEqual(
                self.session.query(TaskQueue).filter_by(task_id=2).first().version,
                datetime.today().strftime('%Y%m%d')+'010102'
        )

        self.assertEqual(self.session.query(TaskQueue).filter_by(task_id=3).all(), [])

        self.assertEqual(
                self.session.query(TaskQueue).filter_by(task_id=4).first().version,
                datetime.today().strftime('%Y%m%d')+'054223'
        )

        self.assertEqual(self.session.query(TaskQueue).filter_by(task_id=5).all(), [])

        self.assertEqual(
                self.session.query(TaskQueue).filter_by(task_id=6).first().version,
                datetime.today().strftime('%Y%m%d')+'173015'
        )

        self.assertEqual(self.session.query(TaskQueue).filter_by(task_id=7).all(), [])

        self.assertEqual(
                self.session.query(TaskQueue).filter_by(task_id=8).first().version,
                datetime.today().strftime('%Y%m%d')+'214500'
        )

        self.assertEqual(self.session.query(TaskQueue).filter_by(task_id=9).all(), [])
        self.assertEqual(self.session.query(TaskQueue).filter_by(task_id=19).all(), [])

        self.assertEqual(self.session.query(TaskQueue).count(), 5)
        self.assertEqual(self.session.query(Task).count(), 10)
        self.assertEqual(self.session.query(Task).filter_by(valid=True).count(), 9)

