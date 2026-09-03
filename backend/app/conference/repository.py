from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Committee, CommitteeAssignment, Conference, ConferenceAssignment
from .schemas import CommitteeCreate, ConferenceCreate


def _conference_from_row(row) -> Conference:
    return Conference(
        id=row["id"],
        name=row["name"],
        status=row["status"],
        owner_id=row["owner_id"],
        location=row["location"],
        logo_url=row["logo_url"],
        theme_color=row["theme_color"],
        start_date=row["start_date"],
        end_date=row["end_date"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def _committee_from_row(row) -> Committee:
    return Committee(
        id=row["id"],
        conference_id=row["conference_id"],
        name=row["name"],
        acronym=row["acronym"],
        committee_type=row["committee_type"],
        logo_url=row["logo_url"],
        theme_color=row["theme_color"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def _committee_assignment_from_row(row) -> CommitteeAssignment:
    return CommitteeAssignment(
        user_id=row["user_id"],
        committee_id=row["committee_id"],
        role=row["role"],
        representation_id=row["representation_id"],
    )


def _conference_assignment_from_row(row) -> ConferenceAssignment:
    return ConferenceAssignment(
        conference_id=row["conference_id"],
        user_id=row["user_id"],
        role=row["role"],
        committee_id=row["committee_id"],
    )


async def create_conference(
    session: AsyncSession,
    *,
    data: ConferenceCreate,
    owner_id: UUID,
) -> Conference | None:
    query = text("""
        INSERT INTO public.conferences
            (name, owner_id, location, logo_url, theme_color, start_date, end_date)
        VALUES
            (:name, :owner_id, :location, :logo_url, :theme_color, :start_date, :end_date)
        RETURNING
            id, name, status, owner_id, location, logo_url, theme_color,
            start_date, end_date, created_at, updated_at
    """)

    result = await session.execute(
        query,
        {
            "name": data.name,
            "owner_id": owner_id,
            "location": data.location,
            "logo_url": data.logo_url,
            "theme_color": data.theme_color,
            "start_date": data.start_date,
            "end_date": data.end_date,
        },
    )
    row = result.mappings().one_or_none()
    return _conference_from_row(row) if row is not None else None


async def create_conference_assignment(
    session: AsyncSession,
    *,
    conference_id: int,
    user_id: UUID,
    role: str,
    committee_id: int | None = None,
) -> None:
    query = text("""
        INSERT INTO public.conference_assignments
            (conference_id, user_id, role, committee_id)
        VALUES
            (:conference_id, :user_id, :role, :committee_id)
        ON CONFLICT DO NOTHING
    """)

    await session.execute(
        query,
        {
            "conference_id": conference_id,
            "user_id": user_id,
            "role": role,
            "committee_id": committee_id,
        },
    )


async def list_user_conferences(
    session: AsyncSession,
    *,
    user_id: UUID,
) -> list[Conference]:
    query = text("""
        SELECT DISTINCT
            c.id, c.name, c.status, c.owner_id, c.location, c.logo_url,
            c.theme_color, c.start_date, c.end_date, c.created_at, c.updated_at
        FROM public.conferences c
        LEFT JOIN public.conference_assignments ca
            ON ca.conference_id = c.id
            AND ca.user_id = :user_id
        WHERE c.owner_id = :user_id
            OR ca.user_id IS NOT NULL
        ORDER BY c.created_at DESC, c.id DESC
    """)

    result = await session.execute(query, {"user_id": user_id})
    return [_conference_from_row(row) for row in result.mappings().all()]


async def get_user_conference(
    session: AsyncSession,
    *,
    conference_id: int,
    user_id: UUID,
) -> Conference | None:
    query = text("""
        SELECT
            c.id, c.name, c.status, c.owner_id, c.location, c.logo_url,
            c.theme_color, c.start_date, c.end_date, c.created_at, c.updated_at
        FROM public.conferences c
        LEFT JOIN public.conference_assignments ca
            ON ca.conference_id = c.id
            AND ca.user_id = :user_id
        WHERE c.id = :conference_id
            AND (
                c.owner_id = :user_id
                OR ca.user_id IS NOT NULL
            )
    """)

    result = await session.execute(
        query, {"conference_id": conference_id, "user_id": user_id}
    )
    row = result.mappings().one_or_none()
    return _conference_from_row(row) if row is not None else None


async def list_user_conference_assignments(
    session: AsyncSession,
    *,
    conference_id: int,
    user_id: UUID,
) -> list[ConferenceAssignment]:
    query = text("""
        SELECT conference_id, user_id, role, committee_id
        FROM public.conference_assignments
        WHERE conference_id = :conference_id
            AND user_id = :user_id
        ORDER BY committee_id NULLS FIRST, role
    """)

    result = await session.execute(
        query, {"conference_id": conference_id, "user_id": user_id}
    )
    return [_conference_assignment_from_row(row) for row in result.mappings().all()]


async def create_committee(
    session: AsyncSession,
    *,
    conference_id: int,
    data: CommitteeCreate,
) -> Committee | None:
    query = text("""
        INSERT INTO public.committees
            (conference_id, name, acronym, committee_type, logo_url, theme_color)
        VALUES
            (
                :conference_id,
                :name,
                :acronym,
                :committee_type,
                :logo_url,
                :theme_color
            )
        RETURNING
            id, conference_id, name, acronym, committee_type, logo_url, theme_color,
            status, created_at, updated_at
    """)

    result = await session.execute(
        query,
        {
            "conference_id": conference_id,
            "name": data.name,
            "acronym": data.acronym,
            "committee_type": data.committee_type,
            "logo_url": data.logo_url,
            "theme_color": data.theme_color,
        },
    )
    row = result.mappings().one_or_none()
    return _committee_from_row(row) if row is not None else None


async def list_conference_committees(
    session: AsyncSession,
    *,
    conference_id: int,
) -> list[Committee]:
    query = text("""
        SELECT
            id, conference_id, name, acronym, committee_type, logo_url, theme_color,
            status, created_at, updated_at
        FROM public.committees
        WHERE conference_id = :conference_id
        ORDER BY created_at DESC, id DESC
    """)

    result = await session.execute(query, {"conference_id": conference_id})
    return [_committee_from_row(row) for row in result.mappings().all()]


async def get_user_committee(
    session: AsyncSession,
    *,
    committee_id: int,
    user_id: UUID,
) -> Committee | None:
    query = text("""
        SELECT
            cm.id, cm.conference_id, cm.name, cm.acronym, cm.committee_type,
            cm.logo_url, cm.theme_color, cm.status, cm.created_at, cm.updated_at
        FROM public.committees cm
        JOIN public.conferences c
            ON c.id = cm.conference_id
        LEFT JOIN public.conference_assignments ca
            ON ca.conference_id = c.id
            AND ca.user_id = :user_id
        WHERE cm.id = :committee_id
            AND (
                c.owner_id = :user_id
                OR ca.user_id IS NOT NULL
            )
    """)

    result = await session.execute(
        query, {"committee_id": committee_id, "user_id": user_id}
    )
    row = result.mappings().one_or_none()
    return _committee_from_row(row) if row is not None else None


async def get_committee_assignment(
    session: AsyncSession,
    *,
    committee_id: int,
    user_id: UUID,
) -> CommitteeAssignment | None:
    query = text("""
        SELECT user_id, committee_id, role, representation_id
        FROM public.committee_assignments
        WHERE committee_id = :committee_id
            AND user_id = :user_id
    """)

    result = await session.execute(
        query, {"committee_id": committee_id, "user_id": user_id}
    )
    row = result.mappings().one_or_none()
    return _committee_assignment_from_row(row) if row is not None else None


async def upsert_committee_session_assignment(
    session: AsyncSession,
    *,
    committee_id: int,
    user_id: UUID,
    role: str,
) -> CommitteeAssignment | None:
    query = text("""
        INSERT INTO public.committee_assignments
            (user_id, committee_id, role, representation_id)
        VALUES
            (:user_id, :committee_id, :role, null)
        ON CONFLICT (user_id, committee_id)
        DO UPDATE SET
            role = EXCLUDED.role,
            representation_id = null
        WHERE public.committee_assignments.role <> 'delegate'
        RETURNING user_id, committee_id, role, representation_id
    """)

    result = await session.execute(
        query,
        {
            "committee_id": committee_id,
            "user_id": user_id,
            "role": role,
        },
    )
    row = result.mappings().one_or_none()
    return _committee_assignment_from_row(row) if row is not None else None
