from pydantic import BaseModel

from . import enums


class SessionRepresentation(BaseModel):
    role: enums.SessionRoles
    representation_id: int | None


class CommitteeScopedConferenceRole(BaseModel):
    committee_id: int
    role: str


class ConferenceAccess(BaseModel):
    conference_id: int
    roles: list[str]
    committee_roles: list[CommitteeScopedConferenceRole]
    can_manage_conference: bool
