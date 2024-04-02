import boto3
from injector import Module, singleton
from omnilife_framework_automations.infrastructure.repositories.parameter import (
    IParameterRepository,
)
from omnilife_framework_automations.parameter.repositories import (
    EnviromentVariableParameterRepository,
    AWSParameterStoreRepository,
)


class EnvironmentVariableParameterRepositoryModule(Module):
    def configure(self, binder):
        binder.bind(
            IParameterRepository,
            to=EnviromentVariableParameterRepository,
            scope=singleton,
        )


class AWSParameterStoreRepositoryModule(Module):
    def configure(self, binder):
        session = boto3.Session()
        binder.bind(
            IParameterRepository,
            to=AWSParameterStoreRepository(session),
            scope=singleton,
        )
