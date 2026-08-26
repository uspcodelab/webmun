from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class ConferenceAssignment:
    """Holds information about a user's role and representation in a conference/committee."""

    user_id: UUID
    role: str
    conference_id: int | None = None
    committee_id: int | None = None
    representation_id: int | None = None


# Alias for backward compatibility if needed by session engine
CommitteeAssignment = ConferenceAssignment

