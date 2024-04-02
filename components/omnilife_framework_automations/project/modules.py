from injector import Module, singleton
from omnilife_framework_automations.infrastructure.repositories.project import (
    IProjectRepository,
)
from omnilife_framework_automations.infrastructure.services import IProjectService
from omnilife_framework_automations.project.repositories import ProjectNotionRepository
from omnilife_framework_automations.project.services import ProjectService


class ProjectServiceModule(Module):
    def configure(self, binder):
        binder.bind(IProjectService, to=ProjectService, scope=singleton)


class ProjectRepositoryModule(Module):
    def configure(self, binder):
        binder.bind(IProjectRepository, to=ProjectNotionRepository, scope=singleton)

