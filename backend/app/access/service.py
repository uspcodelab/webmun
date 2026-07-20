from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.access.models import CommitteeAssignment
from app.session.enums import SessionRole
from .repository import get_committee_assignment

class AccessDenied(Exception):
    ...

async def resolve_committee_assignment(
    session: AsyncSession,
    user_id: UUID,
    session_id: int, 
) -> CommitteeAssignment:
    assignment = await get_committee_assignment(session, user_id, session_id)
    
    if assignment is None: 
        raise AccessDenied("User has no committee assignment")

    if assignment.role == SessionRole.DELEGATE and assignment.delegation_id is None:
        raise AccessDenied("Delegate role has no delegation id")

    return assignment
