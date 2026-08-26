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


class ConferenceSummary(BaseModel):
    """Lightweight conference summary for lists and switchers"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str | None = None
    status: str
    location: str | None = None
    logo: str | None = None
    color: str
    start_date: datetime
    end_date: datetime
    owner_id: UUID
    user_role: str | None = None
    total_committees: int = 0


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


class AssignmentResponse(BaseModel):
    """Schema for returning conference assignment details"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    conference_id: int
    user_id: UUID | None = None
    name: str
    email: str
    institution: str | None = None
    role: str
    committee_id: int | None = None
    representation_id: int | None = None
    created_at: datetime | None = None


class SessionRepresentation(BaseModel):
    """Schema for returning user's role and representation for a session"""

    model_config = ConfigDict(from_attributes=True)

    role: str
    representation_id: int | None = None

