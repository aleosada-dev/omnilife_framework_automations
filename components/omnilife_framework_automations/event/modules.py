from injector import Module, singleton
from omnilife_framework_automations.google.repositories import (
    GoogleCalendarEventRepository,
)
from omnilife_framework_automations.infrastructure.repositories import IEventRespository


class EventRepositoryModule(Module):
    def configure(self, binder):
        binder.bind(
            IEventRespository, to=GoogleCalendarEventRepository, scope=singleton
        )
