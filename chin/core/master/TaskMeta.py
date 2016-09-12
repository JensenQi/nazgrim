from ..models import Task
from .. import DBSession
from VersionController import VersionController


class TaskMeta:

    def __init__(self):
        pass

    @staticmethod
    def add(task):
        session = DBSession()
        session.add(task)
        VersionController.handle_add(task, session)
        session.commit()
        session.close()

    @staticmethod
    def remove(task):
        session = DBSession()
        task = session.query(Task).filter(Task.id == task.id).first()
        task.valid = False
        session.add(task)
        VersionController.handle_remove(task, session)
        session.commit()
        session.close()

    @staticmethod
    def update(task):
        session = DBSession()
        session.add(task)
        VersionController.handle_update(task, session)
        session.commit()
        session.close()
