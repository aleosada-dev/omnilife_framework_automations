import pendulum
from omnilife_framework_automations.event.entities import (
    Event,
    map_googlecalendar_event_to_event,
    safe_get,
)


def test_safe_get_with_existing_keys():
    dictionary = {"a": {"b": {"c": 123}}}
    result = safe_get(dictionary, "a", "b", "c")
    assert result == 123


def test_safe_get_with_missing_keys():
    dictionary = {"a": {"b": {"c": 123}}}
    result = safe_get(dictionary, "x", "y", "z")
    assert result is None


def test_safe_get_with_partial_missing_keys():
    dictionary = {"a": {"b": {"c": 123}}}
    result = safe_get(dictionary, "a", "b", "x")
    assert result is None


def test_safe_get_with_empty_dictionary():
    dictionary = {}
    result = safe_get(dictionary, "a", "b", "c")
    assert result is None


def test_map_googlecalendar_event_to_event_empty_extended_properties():
    google_event = {
        "summary": "Test Event",
        "description": "This is a test event",
        "start": {"dateTime": "2022-01-01T10:00:00Z"},
        "end": {"dateTime": "2022-01-01T12:00:00Z"},
    }

    event = map_googlecalendar_event_to_event(google_event)

    assert isinstance(event, Event)
    assert event.name == "Test Event"
    assert event.description == "This is a test event"
    assert event.start_date == pendulum.datetime(2022, 1, 1, 10, 0, 0, tz="UTC")
    assert event.end_date == pendulum.datetime(2022, 1, 1, 12, 0, 0, tz="UTC")
    assert event.priority is None
    assert event.areas == []


def test_map_googlecalendar_event_to_event():
    google_event = {
        "summary": "Test Event",
        "description": "This is a test event",
        "start": {"dateTime": "2022-01-01T10:00:00Z"},
        "end": {"dateTime": "2022-01-01T12:00:00Z"},
        "extendedProperties": {
            "private": {
                "priority": "High",
                "areas": ["Area 1", "Area 2"],
            }
        },
    }

    event = map_googlecalendar_event_to_event(google_event)

    assert isinstance(event, Event)
    assert event.name == "Test Event"
    assert event.description == "This is a test event"
    assert event.start_date == pendulum.datetime(2022, 1, 1, 10, 0, 0, tz="UTC")
    assert event.end_date == pendulum.datetime(2022, 1, 1, 12, 0, 0, tz="UTC")
    assert event.priority == "High"
    assert event.areas == ["Area 1", "Area 2"]
