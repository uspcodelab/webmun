from typing import Any, Literal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

import app.conference.repository as repository
import app.conference.schemas as schemas
from app.conference.models import ConferenceAssignment
from app.core.exceptions import AccessDeniedError, NotFoundError


async def create_conference(
    session: AsyncSession, user_id: UUID, payload: schemas.ConferenceCreate
) -> int:
    """Create a new conference."""
    conference_id = await repository.create_conference(
        session=session, user_id=user_id, payload=payload
    )
    await session.commit()
    return conference_id


async def get_user_conferences(
    session: AsyncSession, user_id: UUID
) -> list[dict[str, Any]]:
    """Get dashboard summaries for all conferences available to a user."""
    return await repository.get_user_conferences(session=session, user_id=user_id)


async def get_conference_info(
    session: AsyncSession, user_id: UUID, conference_id: int
) -> dict[str, Any]:
    """Get conference detail using split verification and fetch queries."""
    # Query 1: Verification
    user_role = await repository.get_user_conference_role(
        session=session, user_id=user_id, conference_id=conference_id
    )
    if user_role is None:
        raise NotFoundError(f"Conference with id {conference_id} not found")

    # Query 2: Fetch Conference & Committees
    conf = await repository.get_conference_by_id(
        session=session, conference_id=conference_id
    )
    if conf is None:
        raise NotFoundError(f"Conference with id {conference_id} not found")

    committees = await repository.list_committees_for_conference(
        session=session, conference_id=conference_id
    )

    conf["caller_role"] = user_role
    conf["committees"] = committees
    return conf


async def create_committee(
    session: AsyncSession,
    user_id: UUID,
    conference_id: int,
    payload: schemas.CommitteeCreate,
) -> dict[str, Any]:
    """Create a committee within a conference (requires owner/admin role)."""
    user_role = await repository.get_user_conference_role(
        session=session, user_id=user_id, conference_id=conference_id
    )
    if user_role not in ("owner", "admin"):
        raise AccessDeniedError(
            "Only conference owners and admins can create committees"
        )

    committee = await repository.create_committee(
        session=session, conference_id=conference_id, payload=payload
    )
    await session.commit()
    return committee


async def enroll_member(
    session: AsyncSession,
    user_id: UUID,
    conference_id: int,
    payload: schemas.EnrollMember,
) -> dict[str, Any]:
    """Enroll a member or delegate into a conference (requires owner/admin role)."""
    user_role = await repository.get_user_conference_role(
        session=session, user_id=user_id, conference_id=conference_id
    )
    if user_role not in ("owner", "admin"):
        raise AccessDeniedError(
            "Only conference owners and admins can enroll members"
        )

    assignment = await repository.enroll_member(
        session=session, conference_id=conference_id, payload=payload
    )
    await session.commit()
    return assignment


async def list_conference_members(
    session: AsyncSession,
    user_id: UUID,
    conference_id: int,
) -> list[dict[str, Any]]:
    """List all enrolled members in a conference for an authorized user."""
    user_role = await repository.get_user_conference_role(
        session=session, user_id=user_id, conference_id=conference_id
    )
    if user_role is None:
        raise NotFoundError(f"Conference with id {conference_id} not found")

    return await repository.list_conference_members(
        session=session, conference_id=conference_id
    )


def _require_valid_assignment(
    assignment: ConferenceAssignment | None,
) -> ConferenceAssignment:
    """Validate that an assignment grants a usable committee identity."""
    if assignment is None:
        raise AccessDeniedError("User has no assignment for this context")

    if assignment.role == "delegate" and assignment.representation_id is None:
        raise AccessDeniedError("Delegate role has no delegation id")

    return assignment


async def resolve_committee_assignment(
    session: AsyncSession,
    user_id: UUID,
    committee_id: int,
) -> ConferenceAssignment:
    """Resolve a user's assignment for one committee."""
    assignment = await repository.get_committee_assignment(
        session=session,
        user_id=user_id,
        committee_id=committee_id,
    )
    return _require_valid_assignment(assignment)


async def resolve_session_assignment(
    session: AsyncSession,
    user_id: UUID,
    session_id: int,
) -> ConferenceAssignment:
    """Resolve a user's assignment for one committee session."""
    assignment = await repository.get_session_assignment(
        session=session,
        user_id=user_id,
        session_id=session_id,
    )
    return _require_valid_assignment(assignment)


async def verify_user_role(
    session: AsyncSession,
    user_id: UUID,
    committee_id: int,
    required_role: Literal["chair", "delegate"],
) -> ConferenceAssignment:
    """Verify and require that a user has a specific role for a committee."""
    assignment = await resolve_committee_assignment(
        session=session, user_id=user_id, committee_id=committee_id
    )

    if assignment.role != required_role:
        raise AccessDeniedError(
            f"User requires the {required_role} role for this committee"
        )

    return assignment

