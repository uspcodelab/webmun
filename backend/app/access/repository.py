from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from .models import CommitteeAssignment

class AccessRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_committee_assignment(self, user_id: UUID, session_id: int) -> CommitteeAssignment | None:
        query = text("""
            SELECT
                sa.user_id, 
                sa.role,
                sa.delegation_id
            FROM public.sessions s 
            JOIN public.session_assignments sa 
            WHERE s.id = :session_id AND 
            sa.user_id = :user_id
        """)

        result = await self.session.execute(
            query,
            {
                "session_id": session_id,
                "user_id": user_id
            }
        )

        row = result.mappings().one_or_none()
        if row is None:
            return None

        return CommitteeAssignment(
            user_id=row["user_id"],
            session_id=session_id,
            role=row["role"],
            delegation_id=row["delegation_id"]
        )



