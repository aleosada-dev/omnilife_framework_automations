from pprint import pprint
from omnilife_framework_automations.google.repositories import (
    GoogleCalendarEventRepository,
)
from dotenv import load_dotenv
from omnilife_framework_automations.parameter.repositories import (
    EnviromentVariableParameterRepository,
)
import pendulum


load_dotenv()


def test_get_events():
    today = pendulum.now().start_of("day")
    calendar_id = "5677e409133bbe8a6a12ccc0db9741a4d7589a0a1a3477778da3760feb2c4c56@group.calendar.google.com"
    start_min = today.to_iso8601_string()
    start_max = today.add(days=7).to_iso8601_string()

    parameter_repository = EnviromentVariableParameterRepository()
    event_repository = GoogleCalendarEventRepository(parameter_repository)
    events = event_repository.get_events(calendar_id, start_min, start_max)

    for event in events:
        pprint(event)


test_get_events()
