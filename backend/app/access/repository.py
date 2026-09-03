from uuid import UUID

from sqlalchemy import bindparam, text
from sqlalchemy.ext.asyncio import AsyncSession

from .models import AccessibleCommittee, CommitteeAssignment


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


async def has_conference_management_role(
    session: AsyncSession,
    *,
    conference_id: int,
    user_id: UUID,
    roles: set[str],
) -> bool:
    query = text("""
        SELECT 1
        FROM public.conferences c
        LEFT JOIN public.conference_assignments ca
            ON ca.conference_id = c.id
            AND ca.user_id = :user_id
            AND ca.role IN :roles
        WHERE c.id = :conference_id
            AND (
                c.owner_id = :user_id
                OR ca.user_id IS NOT NULL
            )
        LIMIT 1
    """).bindparams(bindparam("roles", expanding=True))

    result = await session.execute(
        query,
        {
            "conference_id": conference_id,
            "user_id": user_id,
            "roles": list(roles),
        },
    )
    return result.scalar_one_or_none() is not None


async def has_conference_assignment_for_session_access(
    session: AsyncSession,
    *,
    conference_id: int,
    committee_id: int,
    user_id: UUID,
    roles: set[str],
) -> bool:
    query = text("""
        SELECT 1
        FROM public.committees cm
        JOIN public.conference_assignments ca
            ON ca.conference_id = cm.conference_id
            AND ca.user_id = :user_id
            AND ca.role IN :roles
            AND (
                ca.committee_id IS NULL
                OR ca.committee_id = cm.id
            )
        WHERE cm.id = :committee_id
            AND cm.conference_id = :conference_id
        LIMIT 1
    """).bindparams(bindparam("roles", expanding=True))

    result = await session.execute(
        query,
        {
            "conference_id": conference_id,
            "committee_id": committee_id,
            "user_id": user_id,
            "roles": list(roles),
        },
    )
    return result.scalar_one_or_none() is not None


async def list_accessible_conference_committees(
    session: AsyncSession,
    *,
    conference_id: int,
    user_id: UUID,
    conference_roles: set[str],
) -> list[AccessibleCommittee]:
    query = text("""
        SELECT DISTINCT ON (committee_id)
            committee_id,
            role,
            representation_id
        FROM (
            SELECT
                ca.committee_id,
                ca.role::text AS role,
                ca.representation_id,
                CASE
                    WHEN ca.role::text = 'delegate' THEN 1
                    WHEN ca.role::text = 'chair' THEN 2
                    ELSE 3
                END AS priority
            FROM public.committee_assignments ca
            JOIN public.committees cm
                ON cm.id = ca.committee_id
            WHERE cm.conference_id = :conference_id
                AND ca.user_id = :user_id

            UNION ALL

            SELECT
                cm.id AS committee_id,
                'chair' AS role,
                null::bigint AS representation_id,
                2 AS priority
            FROM public.committees cm
            JOIN public.conferences c
                ON c.id = cm.conference_id
            LEFT JOIN public.conference_assignments cfa
                ON cfa.conference_id = c.id
                AND cfa.user_id = :user_id
                AND cfa.role IN :conference_roles
                AND (
                    cfa.committee_id IS NULL
                    OR cfa.committee_id = cm.id
                )
            WHERE cm.conference_id = :conference_id
                AND (
                    c.owner_id = :user_id
                    OR cfa.user_id IS NOT NULL
                )
        ) access
        ORDER BY committee_id, priority
    """).bindparams(bindparam("conference_roles", expanding=True))

    result = await session.execute(
        query,
        {
            "conference_id": conference_id,
            "user_id": user_id,
            "conference_roles": list(conference_roles),
        },
    )

    return [
        AccessibleCommittee(
            committee_id=row["committee_id"],
            role=row["role"],
            representation_id=row["representation_id"],
        )
        for row in result.mappings().all()
    ]
