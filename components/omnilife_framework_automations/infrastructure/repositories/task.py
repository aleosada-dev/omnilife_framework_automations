from omnilife_framework_automations.task.entities import Task
from abc import abstractmethod


class ITaskRepository:
    @abstractmethod
    def add_task(self, task: Task):
        raise NotImplementedError
