import pendulum
from dataclasses import dataclass
from functools import reduce


@dataclass
class Event:
    name: str
    description: str
    start_date: pendulum.DateTime
    end_date: pendulum.DateTime
    areas: list
    priority: str


def safe_get(dictionary, *keys):
    return reduce(lambda d, k: d.get(k) if d else None, keys, dictionary)


def map_googlecalendar_event_to_event(google_event):
    start_date = safe_get(google_event, "start", "dateTime")
    if start_date:
        start_date = pendulum.parse(start_date)
    end_date = safe_get(google_event, "end", "dateTime")
    if end_date:
        end_date = pendulum.parse(end_date)
    priority = safe_get(google_event, "extendedProperties", "private", "priority")

    event = Event(
        name=google_event.get("summary"),
        description=google_event.get("description"),
        start_date=start_date,
        end_date=end_date,
        priority=priority,
        areas=[],
    )

    areas = safe_get(google_event, "extendedProperties", "private", "areas")
    if areas:
        if isinstance(areas, str):
            event.areas.append(areas)
        if isinstance(areas, list):
            for area in areas:
                event.areas.append(area)

    return event
