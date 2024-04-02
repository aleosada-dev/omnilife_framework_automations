from injector import Module, singleton
from omnilife_framework_automations.google.repositories import (
    GoogleCalendarEventRepository,
)
from omnilife_framework_automations.infrastructure.repositories.event import (
    IEventRepository,
)


class EventRepositoryModule(Module):
    def configure(self, binder):
        binder.bind(IEventRepository, to=GoogleCalendarEventRepository, scope=singleton)
