from app.access.models import CommitteeAssignment
from app.session.schemas import DelegationSchema
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from .models import DelegationContext


class SessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


async def create_session(
    session: AsyncSession, name: str, delegations: list[DelegationContext]
) -> int | None:
    """Creates a session on db"""

    query = text("""
        INSERT INTO public.sessions
            (name, delegations_config)
        VALUES
            (:name, :delegations_list)
        RETURNING id
   """)

    result = await session.execute(
        query,
        {
            "name": name,
            "delegations_list": [
                delegation.model_dump(mode="json") for delegation in delegations
            ],
        },
    )

    row = result.mappings().one_or_none()
    if row is None:
        return None

    return row["id"]


async def bulk_get_uuids_by_email(
    session: AsyncSession, delegations_schema: list[DelegationSchema]
):
    """Searches an uuid via email on supabase auth"""

    # selects all (id, email) rows mapping out emails
    query = text("""
        SELECT email, id
        FROM auth.users
        WHERE email = ANY(:emails)
    """)

    result = await session.execute(
        query, {"emails": [d.user_email for d in delegations_schema]}
    )

    return {r["email"]: r["id"] for r in result.mappings().all()}


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
        INSERT INTO public.session_assignments (user_id, session_id, role, delegation_id)
        VALUES (:user_id, :session_id, :role, :delegation_id)
    """)

    await session.execute(
        query,
        params,
    )
