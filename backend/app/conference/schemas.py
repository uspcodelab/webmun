from datetime import datetime

from pydantic import BaseModel


class ConferenceCreate(BaseModel):
    """Schema for conference creation"""

    name: str
    location: str | None = None
    color: str = "#0f172a"
    start_date: datetime
    end_date: datetime


class EnrollMember(BaseModel):
    """Schema for enrolling a user into a conference"""

    name: str
    email: str
    role: str = "delegate"
    committee_id: int | None = None
    representation_id: int | None = None


class CommitteeCreate(BaseModel):
    """Schema for creating a committee"""

    ...
