import pytest
from unittest.mock import Mock, patch

from omnilife_framework_automations.google.repositories import (
    GoogleCalendarEventRepository,
)


@pytest.fixture
def event1():
    return {
        "summary": "Event 1",
        "description": "Description 1",
        "start": {"dateTime": "2021-01-01T00:00:00-06:00"},
        "end": {"dateTime": "2021-01-01T01:00:00-06:00"},
        "extendedProperties": {
            "private": {
                "priority": "high",
                "areas": ["area1", "area2"],
            }
        },
    }


@pytest.fixture
def event2():
    return {
        "summary": "Event 2",
        "description": "Description 2",
        "start": {"dateTime": "2021-01-02T00:00:00-06:00"},
        "end": {"dateTime": "2021-01-02T01:00:00-06:00"},
        "extendedProperties": {
            "private": {
                "priority": "low",
                "areas": "area3",
            }
        },
    }


@pytest.fixture
def events_result(event1, event2):
    return {"items": [event1, event2]}


@pytest.mark.skip
def test_get_events(events_result):
    # Mock the parameter repository
    parameter_repository = Mock()
    parameter_repository.get.side_effect = [
        "project_id",
        "private_key_id",
        "private_key",
        "client_email",
        "client_id",
        "client_x509_cert_url",
    ]

    # Create an instance of the repository
    repository = GoogleCalendarEventRepository(parameter_repository)

    # Mock the service and events
    service = Mock()
    events = Mock()
    events.list.return_value.execute.return_value = events_result
    service.events.return_value = events

    # Mock the build function
    build = Mock(return_value=service)

    # Patch the build function
    with patch("omnilife_framework_automations.google.repositories.build", build):
        # Call the get_events method
        result = repository.get_events("calendar_id", "start_min", "start_max")

    # Assert the expected calls and results
    parameter_repository.get.assert_called_with("GOOGLE_CALENDAR_PROJECT_ID")
    build.assert_called_with("calendar", "v3", credentials=Mock())
    events.list.assert_called_with(
        calendarId="calendar_id",
        singleEvents=False,
        timeMin="start_min",
        timeMax="start_max",
        showDeleted=False,
    )
    events.list.return_value.execute.assert_called()
    assert result == [event1, event2]
