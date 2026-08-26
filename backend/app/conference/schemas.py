from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ConferenceCreate(BaseModel):
    """Schema for conference creation"""

    name: str
    slug: str | None = None
    location: str | None = None
    logo: str | None = None
    color: str = "#0f172a"
    start_date: datetime
    end_date: datetime


class CommitteeCreate(BaseModel):
    """Schema for creating a committee"""

    name: str
    code: str
    logo: str | None = None
    topic: str | None = None
    status: str = "planned"


class CommitteeResponse(BaseModel):
    """Schema for returning committee details"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    conference_id: int
    name: str
    code: str
    logo: str | None = None
    topic: str | None = None
    status: str
    created_at: datetime | None = None


class ConferenceSummary(BaseModel):
    """Conference data needed to select a conference in the dashboard."""

    id: int
    name: str
    logo: str | None = None
    color: str
    status: str
    caller_role: str


class ConferenceDetail(BaseModel):
    """Detailed conference information including its committees"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str | None = None
    status: str
    owner_id: UUID
    location: str | None = None
    logo: str | None = None
    color: str
    start_date: datetime
    end_date: datetime
    caller_role: str | None = None
    committees: list[CommitteeResponse] = []


class EnrollMember(BaseModel):
    """Schema for enrolling/assigning a user into a conference"""

    name: str
    email: str
    institution: str | None = None
    role: str = "participant"
    committee_id: int | None = None
    representation_id: int | None = None
