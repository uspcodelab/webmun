from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ConferenceAssignment(BaseModel):
    """Holds information about a user's role, enrollment, and representation."""

    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    conference_id: int | None = None
    user_id: UUID | None = None
    name: str | None = None
    email: str | None = None
    institution: str | None = None
    role: str
    committee_id: int | None = None
    representation_id: int | None = None
    created_at: datetime | None = None



