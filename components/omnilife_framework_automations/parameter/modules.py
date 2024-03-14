from injector import Module, singleton
from omnilife_framework_automations.infrastructure.repositories import (
    IParameterRepository,
)
from omnilife_framework_automations.parameter.repositories import (
    EnviromentVariableParameterRepository,
)


class ParameterRepositoryModule(Module):
    def configure(self, binder):
        binder.bind(
            IParameterRepository,
            to=EnviromentVariableParameterRepository,
            scope=singleton,
        )
