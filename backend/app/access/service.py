from typing import Literal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.access.models import CommitteeAssignment
from app.access.schemas import (
    AccessibleCommittee,
    CommitteeScopedConferenceRole,
    ConferenceAccess,
)
from app.conference import repository as conference_repository
from app.conference.enums import ConferenceRole
from app.core.exceptions import AccessDeniedError

from .repository import (
    get_committee_assignment,
    get_session_assignment,
    has_conference_assignment_for_session_access,
    has_conference_management_role,
    list_accessible_conference_committees,
)

CONFERENCE_MANAGEMENT_ROLES = {
    "owner",
    "secretary_general",
}

SESSION_ACCESS_GRANTING_CONFERENCE_ROLES = {
    "owner",
    "secretary_general",
    "director",
    "moderator",
}


async def resolve_committee_assignment(
    session: AsyncSession,
    user_id: UUID,
    committee_id: int,
) -> CommitteeAssignment:
    assignment: CommitteeAssignment | None = await get_committee_assignment(
        session, user_id, committee_id
    )

    if assignment is None:
        raise AccessDeniedError("User has no committee assignment")

    if assignment.role == "delegate" and assignment.representation_id is None:
        raise AccessDeniedError("Delegate role has no delegation id")

    return assignment


async def resolve_session_assignment(
    session: AsyncSession,
    user_id: UUID,
    session_id: int,
) -> CommitteeAssignment:
    """Resolve the assignment for a session without trusting client committee data."""
    assignment = await get_session_assignment(session, user_id, session_id)

    if assignment is None:
        raise AccessDeniedError("User has no assignment for this session")

    if assignment.role == "delegate" and assignment.representation_id is None:
        raise AccessDeniedError("Delegate role has no delegation id")

    return assignment


async def verify_user_role(
    session: AsyncSession,
    user_id: UUID,
    committee_id: int,
    required_role: Literal["chair", "delegate"],
) -> CommitteeAssignment:
    """Require a user's role within one specific committee."""
    assignment = await get_committee_assignment(session, user_id, committee_id)

    if assignment is None:
        raise AccessDeniedError("User has no committee assignment")

    if assignment.role != required_role:
        raise AccessDeniedError(
            f"User requires the {required_role} role for this committee"
        )

    return assignment


async def verify_can_manage_conference(
    session: AsyncSession,
    user_id: UUID,
    conference_id: int,
) -> None:
    # TODO: split conference/dashboard access from live-session access as this grows.
    can_manage = await has_conference_management_role(
        session=session,
        conference_id=conference_id,
        user_id=user_id,
        roles=CONFERENCE_MANAGEMENT_ROLES,
    )
    if not can_manage:
        raise AccessDeniedError("User cannot manage this conference")


async def get_my_conference_access(
    session: AsyncSession,
    user_id: UUID,
    conference_id: int,
) -> ConferenceAccess:
    conference = await conference_repository.get_user_conference(
        session=session,
        conference_id=conference_id,
        user_id=user_id,
    )
    if conference is None:
        raise AccessDeniedError("User has no access to this conference")

    assignments = await conference_repository.list_user_conference_assignments(
        session=session,
        conference_id=conference_id,
        user_id=user_id,
    )

    roles = sorted(
        {
            assignment.role
            for assignment in assignments
            if assignment.committee_id is None
        }
    )
    if conference.owner_id == user_id and ConferenceRole.OWNER.value not in roles:
        roles.append(ConferenceRole.OWNER.value)

    committee_roles = [
        CommitteeScopedConferenceRole(
            committee_id=assignment.committee_id,
            role=assignment.role,
        )
        for assignment in assignments
        if assignment.committee_id is not None
    ]
    accessible_committees = [
        AccessibleCommittee(
            committee_id=committee.committee_id,
            role=committee.role,
            representation_id=committee.representation_id,
        )
        for committee in await list_accessible_conference_committees(
            session=session,
            conference_id=conference_id,
            user_id=user_id,
            conference_roles=SESSION_ACCESS_GRANTING_CONFERENCE_ROLES,
        )
    ]

    return ConferenceAccess(
        conference_id=conference_id,
        roles=roles,
        committee_roles=committee_roles,
        accessible_committees=accessible_committees,
        can_manage_conference=any(
            role in CONFERENCE_MANAGEMENT_ROLES for role in roles
        ),
    )


async def verify_conference_assignment_can_grant_session_access(
    session: AsyncSession,
    user_id: UUID,
    conference_id: int,
    committee_id: int,
) -> None:
    # TODO: keep role policy centralized here as conference/team access grows.
    can_grant = await has_conference_assignment_for_session_access(
        session=session,
        conference_id=conference_id,
        committee_id=committee_id,
        user_id=user_id,
        roles=SESSION_ACCESS_GRANTING_CONFERENCE_ROLES,
    )
    if not can_grant:
        raise AccessDeniedError(
            "Conference assignment cannot grant committee session access"
        )
