# coding=utf-8
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

        rerun_task = Task(
                user='root',
                command='shell /home/suit/rerun_task.sh',
                machine_pool=['slave_1', 'slave_2', 'slave_3'],
                valid=True,
                rerun=True,
                rerun_times=2,
                scheduled_type='day',
                hour=10, minute=11, second=12
        )

        unrerun_task = Task(
                user='root',
                command='shell /home/suit/rerun_task.sh',
                machine_pool=['slave_4', 'slave_5', 'slave_6'],
                valid=True,
                scheduled_type='week',
                weekday=datetime.now().isoweekday(),
                hour=18, minute=19, second=20
        )

        TaskMeta.add(rerun_task).by(self.session)
        TaskMeta.add(unrerun_task).by(self.session)
        self.session.commit()

    def tearDown(self):
        self.session.close()

    def test_serve(self):
        # 启动版本号服务
        self.version_controller.serve()
        time.sleep(2)

        rerun_task = self.session.query(TaskQueue).filter_by(id=1).first()
        unrerun_task = self.session.query(TaskQueue).filter_by(id=2).first()


        # 确认任务未分配
        self.assertEqual(rerun_task.status, None)
        self.assertEqual(rerun_task.execute_machine, None)
        self.assertEqual(rerun_task.run_count, 0)
        self.assertEqual(unrerun_task.status, None)
        self.assertEqual(unrerun_task.execute_machine, None)
        self.assertEqual(unrerun_task.run_count, 0)

        # 启动任务分发服务
        self.task_distributor.serve()
        time.sleep(2)

        # 确认任务分发成功
        self.session.commit()
        self.assertNotEqual(rerun_task.execute_machine, None)
        self.assertEqual(rerun_task.status, 'waiting')
        self.assertEqual(rerun_task.run_count, 1)
        self.assertNotEqual(unrerun_task.execute_machine, None)
        self.assertEqual(unrerun_task.status, 'waiting')
        self.assertEqual(unrerun_task.run_count, 1)

        # 测试可重跑任务
        # 第一次: slave放弃执行
        rerun_task.status = 'abandon'
        self.session.add(rerun_task)
        self.assertEqual(rerun_task.status, 'abandon')
        self.session.commit()
        time.sleep(2)
        self.assertEqual(rerun_task.status, 'waiting')
        self.assertEqual(rerun_task.run_count, 2)

        # 第二次: 执行失败
        rerun_task.status = 'failed'
        self.session.add(rerun_task)
        self.assertEqual(rerun_task.status, 'failed')
        self.session.commit()
        time.sleep(2)
        self.assertEqual(rerun_task.status, 'waiting')
        self.assertEqual(rerun_task.run_count, 3)

        # 第三次: 超出重试次数
        rerun_task.status = 'failed'
        self.session.add(rerun_task)
        self.assertEqual(rerun_task.status, 'failed')
        self.session.commit()
        time.sleep(2)
        self.assertEqual(rerun_task.status, 'failed')
        self.assertEqual(rerun_task.run_count, 3)

        # 测试不可重跑任务
        unrerun_task.status = 'failed'
        self.session.add(unrerun_task)
        self.assertEqual(unrerun_task.status, 'failed')
        self.session.commit()
        time.sleep(2)
        self.assertEqual(unrerun_task.status, 'failed')
        self.assertEqual(unrerun_task.run_count, 1)

