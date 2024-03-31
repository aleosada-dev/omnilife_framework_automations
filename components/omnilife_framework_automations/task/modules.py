from typing import Self
from injector import Binder, Module, singleton
from omnilife_framework_automations.infrastructure.repositories import ITaskRepository
from omnilife_framework_automations.infrastructure.services import ITaskService
from omnilife_framework_automations.task.repositories import TaskNotionRepository
from omnilife_framework_automations.task.services import TaskService


class TaskRepositoryModule(Module):
    def configure(self: Self, binder: Binder):
        binder.bind(ITaskRepository, to=TaskNotionRepository, scope=singleton)


class TaskServiceModule(Module):
    def configure(self: Self, binder: Binder) -> None:
        binder.bind(ITaskService, to=TaskService, scope=singleton)
