from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from .models import CommitteeAssignment

# TODO: pass this to a conference/ domain
async def get_committee_assignment(
    session: AsyncSession, user_id: UUID, committee_id: int
) -> CommitteeAssignment | None:
    query = text("""
        SELECT
            ca.user_id,
            ca.committee_id,
            ca.role,
            ca.representation_id
        FROM public.committees c 
        JOIN public.committee_assignments ca 
        ON c.id = ca.committee_id
        WHERE c.id = :committee_id AND 
        ca.user_id = :user_id
    """)

    result = await session.execute(
        query, {"committee_id": committee_id, "user_id": user_id}
    )

    row = result.mappings().one_or_none()
    if row is None:
        return None

    return CommitteeAssignment(
        user_id=row["user_id"],
        committee_id=row["committee_id"],
        role=row["role"],
        representation_id=row["representation_id"],
    )


async def get_session_assignment(
    session: AsyncSession, user_id: UUID, session_id: int
) -> CommitteeAssignment | None:
    """Get a user's assignment for the committee that owns a session."""
    query = text("""
        SELECT
            ca.user_id,
            ca.committee_id,
            ca.role,
            ca.representation_id
        FROM public.sessions s
        JOIN public.committee_assignments ca
            ON ca.committee_id = s.committee_id
        WHERE s.id = :session_id
          AND ca.user_id = :user_id
    """)

    result = await session.execute(
        query, {"session_id": session_id, "user_id": user_id}
    )
    row = result.mappings().one_or_none()
    if row is None:
        return None

    return CommitteeAssignment(
        user_id=row["user_id"],
        committee_id=row["committee_id"],
        role=row["role"],
        representation_id=row["representation_id"],
    )
