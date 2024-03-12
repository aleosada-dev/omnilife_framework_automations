import pendulum
from dataclasses import dataclass


@dataclass
class Event:
    name: str
    description: str
    start_date: pendulum.DateTime
    end_date: pendulum.DateTime
    areas: list
    priority: str
