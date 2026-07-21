from sqlalchemy.exc import SQLAlchemyError

from app.access.models import CommitteeAssignment
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.session.models import DelegationContext, StoredSession

class RepositoryError(Exception):
    """Base exception for all repository issues"""
    pass

async def create_session(
    session: AsyncSession, 
    committee_id: int,
    name: str | None,
) -> int | None:
    """Creates a planned session on repository"""

    query = text("""
        INSERT INTO public.sessions
            (committee_id, name)
        VALUES
            (:committee_id, :name)
        RETURNING id
   """)

    result = await session.execute(
        query,
        { "name": name, "committee_id": committee_id }
    )

    row = result.mappings().one_or_none()
    if row is None:
        return None

    return row["id"]

async def get_session_info(
    session: AsyncSession,
    committee_session_id: int
) -> StoredSession | None:
    """Gets info for a session"""
    query = text("""
        SELECT * FROM public.sessions s
        WHERE s.id = :committee_session_id
    """)

    result = await session.execute(
        query, 
        {"committee_session_id": committee_session_id},
    )

    row = result.mappings().one_or_none()
    if row is None:
        return None 

    return StoredSession(
        id=row["id"], 
        committee_id=row["committee_id"],
        name=row["name"],
        status=row["status"],
        started_at=row["started_at"],
        ended_at=row["ended_at"],
        state_snapshot=row["state_snapshot"]
    )

async def update_session_info(
    session: AsyncSession,
    session_info: StoredSession,
) -> None:
    query = text("""
        UPDATE public.sessions
        SET 
            name = :name, 
            status = :status, 
            started_at = :started_at, 
            ended_at = :ended_at, 
            state_snapshot = :state_snapshot
        WHERE id = :committee_session_id
    """)
    
    try:
        await session.execute(
            query,
            {
                "name": session_info.name,
                "status": session_info.status,
                "started_at": session_info.started_at,
                "ended_at": session_info.ended_at,
                "state_snapshot": session_info.state_snapshot,
                "committee_session_id": session_info.id
            }
        )
    except SQLAlchemyError: 
        raise RepositoryError("Session update failed")


async def bulk_insert_assignments(
    session: AsyncSession, delegations: list[CommitteeAssignment]
):
    """Inserts via bulk all (uuid, delegation, session_id) rows"""
    params = [
        {
            "user_id": d.user_id,
            "session_id": d.session_id,
            "role": d.role,
            "delegation_id": d.delegation_id,
        }
        for d in delegations
    ]

    query = text("""
        INSERT INTO public.committee_assignments (user_id, committee_id, role, representation_id)
        VALUES (:user_id, :session_id, :role, :delegation_id)
    """)

    await session.execute(
        query,
        params,
    )

# TODO: pass this out to conferences/ domain
async def bulk_get_delegation_context(
    session: AsyncSession,
    committee_id: int,
) -> list[DelegationContext] | None:
    """
    Get by bulk a list of representations to insert in the live state
    Note: this returns a list of DelegationContext. This is not ideal. 
    We need a clear separation between delegation name/code and the map. 
    Since it's not what we have for now, we'll keep this here
    """

    representation_query = text("""
        SELECT r.id, r.name, r.code, c.seat_label as seat
        FROM public.representations r
        JOIN public.committee_seats c 
        ON r.id = c.representation_id
        WHERE c.committee_id = :committee_id
    """)


    result = await session.execute(
        representation_query, 
        {"committee_id": committee_id}
    )

    if result is None:
        return None
    
    return [DelegationContext(
                id=r["id"], 
                name=r["name"], 
                seat=r["seat"], 
                code=r["code"])
            for r in result.mappings().all()]



