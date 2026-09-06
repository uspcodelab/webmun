from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .enums import ConferenceRole


class ConferenceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    location: str | None = Field(default=None, max_length=255)
    logo_url: str | None = Field(default=None, max_length=1000)
    theme_color: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
    start_date: datetime | None = None
    end_date: datetime | None = None


class ConferenceRead(BaseModel):
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


class CommitteeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    acronym: str | None = Field(default=None, max_length=16)
    committee_type: str | None = Field(default=None, max_length=64)
    logo_url: str | None = Field(default=None, max_length=1000)
    theme_color: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
    layout_id: int = Field(gt=0)


class CommitteeRead(BaseModel):
    id: int
    conference_id: int
    name: str
    acronym: str | None
    committee_type: str | None
    logo_url: str | None
    theme_color: str | None
    status: str
    created_at: datetime
    updated_at: datetime


class CommitteeAssignmentRead(BaseModel):
    user_id: UUID
    committee_id: int
    role: str
    representation_id: int | None


class ConferenceAssignmentCreate(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    role: ConferenceRole
    committee_id: int | None = None


class ConferenceAssignmentRead(BaseModel):
    conference_id: int
    email: str
    role: ConferenceRole
    committee_id: int | None


class ParticipantAllocationCreate(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    committee_id: int
    representation_id: int


class ParticipantAllocationRead(BaseModel):
    email: str
    committee_id: int | None
    committee_name: str | None
    representation_id: int | None
    representation_name: str | None


class RepresentationRead(BaseModel):
    id: int
    name: str
    code: str | None


class LayoutRead(BaseModel):
    id: int
    name: str
