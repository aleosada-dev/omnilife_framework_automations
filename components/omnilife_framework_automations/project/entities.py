from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class ProjectStatus(Enum):
    NOT_STARTED = "Not started"
    IN_PROGRESS = "In progress"
    DONE = "Done"


@dataclass(frozen=True, eq=True)
class Project:
    id: int
    name: str
    area: str
    status: str
    start_date: datetime
    end_date: datetime 
    created_at: datetime
    last_edit_at: datetime