from ..models import Task
from VersionController import VersionController


class TaskMeta:
    def __init__(self):
        pass

    @staticmethod
    def add(task, session):
        session.add(task)
        VersionController.handle_add(task, session)
        session.commit()

    @staticmethod
    def remove(task, session):
        task = session.query(Task).filter(Task.id == task.id).first()
        task.valid = False
        session.add(task)
        VersionController.handle_remove(task, session)
        session.commit()

    @staticmethod
    def update(task, session):
        session.add(task)
        VersionController.handle_update(task, session)
        session.commit()
