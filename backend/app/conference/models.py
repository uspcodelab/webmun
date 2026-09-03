from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Conference:
    id: int
    name: str
    status: str
    owner_id: UUID | None
    location: str | None
    logo_url: str | None
    theme_color: str | None
    start_date: datetime | None
    end_date: datetime | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class Committee:
    id: int
    conference_id: int
    name: str
    status: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class CommitteeAssignment:
    user_id: UUID
    committee_id: int
    role: str
    representation_id: int | None


@dataclass(frozen=True)
class ConferenceAssignment:
    conference_id: int
    user_id: UUID
    role: str
    committee_id: int | None
