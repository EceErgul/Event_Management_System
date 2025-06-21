# Data structures (optional, for clarity or type hinting)

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Department:
    DepartmentID: int
    DepartmentName: str

@dataclass
class Organizer:
    OrganizerID: int
    Name: str
    Email: Optional[str]
    DepartmentID: int

@dataclass
class Participant:
    ParticipantID: int
    Name: str
    Email: Optional[str]
    Contact: Optional[str]
    DepartmentID: int

@dataclass
class Event:
    EventID: int
    Name: str
    Date: datetime
    Location: Optional[str]
    Description: Optional[str]
    OrganizerID: int

@dataclass
class Registration:
    RegistrationID: int
    EventID: int
    ParticipantID: int
    Status: Optional[str]
    Attendance: Optional[bool]
    RegistrationDate: Optional[datetime]