from pydantic import BaseModel

from . import enums


class SessionRepresentation(BaseModel):
    role: enums.SessionRoles
    representation_id: int | None


class CommitteeScopedConferenceRole(BaseModel):
    committee_id: int
    role: str


class AccessibleCommittee(BaseModel):
    committee_id: int
    role: str
    representation_id: int | None


class ConferenceAccess(BaseModel):
    conference_id: int
    roles: list[str]
    committee_roles: list[CommitteeScopedConferenceRole]
    accessible_committees: list[AccessibleCommittee]
    can_manage_conference: bool
