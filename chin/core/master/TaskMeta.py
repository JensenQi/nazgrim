from ..models import Task
from VersionController import VersionController


class TaskMeta:
    def __init__(self):
        pass

    @staticmethod
    def add(task):
        return Deal('add', task)

    @staticmethod
    def remove(task):
        return Deal('remove', task)

    @staticmethod
    def update(task):
        return Deal('update', task)


class Deal:
    def __init__(self, action, task):
        self.task = task
        self.action = action

    def by(self, session):
        if self.action == 'add':
            VersionController.handle_add(self.task, session)
        if self.action == 'remove':
            self.task = session.query(Task).filter(Task.id == self.task.id).first()
            self.task.valid = False
            VersionController.handle_remove(self.task, session)
        if self.action == 'update':
            VersionController.handle_update(self.task, session)
        session.add(self.task)
        session.commit()
