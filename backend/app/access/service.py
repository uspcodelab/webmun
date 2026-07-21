from typing import Literal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.access.models import CommitteeAssignment
from .repository import get_committee_assignment


class AccessDenied(Exception): ...


async def resolve_committee_assignment(
    session: AsyncSession,
    user_id: UUID,
    committee_id: int,
) -> CommitteeAssignment:
    assignment: CommitteeAssignment | None = await get_committee_assignment(
        session, user_id, committee_id
    )

    if assignment is None:
        raise AccessDenied("User has no committee assignment")

    if assignment.role == 'delegate' and assignment.representation_id is None:
        raise AccessDenied("Delegate role has no delegation id")

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
        raise AccessDenied("User has no committee assignment")

    if assignment.role != required_role:
        raise AccessDenied(
            f"User requires the {required_role} role for this committee"
        )

    return assignment
