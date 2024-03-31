from typing import Self
from googleapiclient.discovery import build
from google.oauth2 import service_account
from injector import inject
from omnilife_framework_automations.event.entities import (
    map_googlecalendar_event_to_event,
)
from omnilife_framework_automations.infrastructure.repositories import (
    IParameterRepository,
)


class GoogleCalendarEventRepository:
    @inject
    def __init__(self: Self, parameter_respository: IParameterRepository) -> None:
        self.parameter_repository = parameter_respository

    def get_events(self: Self, calendar_id: str, start_min: str, start_max: str):
        project_id = self.parameter_repository.get("GOOGLE_PROJECT_ID")
        private_key_id = self.parameter_repository.get("GOOGLE_PRIVATE_KEY_ID")
        private_key = self.parameter_repository.get("GOOGLE_PRIVATE_KEY").replace(
            "\\n", "\n"
        )
        client_email = self.parameter_repository.get("GOOGLE_CLIENT_EMAIL")
        client_id = self.parameter_repository.get("GOOGLE_CLIENT_ID")
        client_x509_cert_url = self.parameter_repository.get(
            "GOOGLE_CLIENT_X509_CERT_URL"
        )

        credentials = service_account.Credentials.from_service_account_info(
            {
                "type": "service_account",
                "project_id": project_id,
                "private_key_id": private_key_id,
                "private_key": private_key,
                "client_email": client_email,
                "client_id": client_id,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": client_x509_cert_url,
            }
        )

        service = build("calendar", "v3", credentials=credentials)

        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                singleEvents=True,
                timeMin=start_min,
                timeMax=start_max,
                showDeleted=False,
            )
            .execute()
        )

        return [
            map_googlecalendar_event_to_event(e)
            for e in events_result.get("items", [])
            if e.get("status") != "cancelled"
        ]
