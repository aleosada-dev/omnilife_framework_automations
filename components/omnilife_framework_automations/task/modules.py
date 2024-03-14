from injector import Module, singleton
from omnilife_framework_automations.infrastructure.repositories import ITaskRepository
from omnilife_framework_automations.task.repositories import TaskNotionRepository


class TaskRepositoryModule(Module):
    def configure(self, binder):
        binder.bind(ITaskRepository, to=TaskNotionRepository, scope=singleton)
