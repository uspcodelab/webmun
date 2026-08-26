import json
from typing import Any
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.conference import schemas
from app.conference.models import ConferenceAssignment


async def create_conference(
    session: AsyncSession, user_id: UUID, payload: schemas.ConferenceCreate
) -> int:
    """Create a new conference and return its id."""
    query = text("""
        INSERT INTO public.conferences
            (name, slug, owner_id, location, logo, color, start_date, end_date)
        VALUES (
            :name,
            :slug,
            :owner_id,
            :location,
            :logo,
            :color,
            :start_date,
            :end_date
        )
        RETURNING id
    """)

    result = await session.execute(
        query,
        {
            "name": payload.name,
            "slug": payload.slug,
            "owner_id": user_id,
            "location": payload.location,
            "logo": payload.logo,
            "color": payload.color,
            "start_date": payload.start_date,
            "end_date": payload.end_date,
        },
    )
    row = result.mappings().one()
    return int(row["id"])


async def get_user_conferences(
    session: AsyncSession,
    user_id: UUID,
) -> list[int]:
    """Return all conference IDs where the user is an owner or assigned member."""
    query = text("""
        SELECT DISTINCT c.id
        FROM public.conferences c
        LEFT JOIN public.conference_assignments ca 
            ON ca.conference_id = c.id AND ca.user_id = :user_id
        WHERE c.owner_id = :user_id OR ca.user_id = :user_id
        ORDER BY c.id ASC
    """)

    result = await session.execute(query, {"user_id": user_id})
    return [int(r["id"]) for r in result.mappings().all()]


async def get_conference_by_id(
    session: AsyncSession,
    conference_id: int,
) -> dict[str, Any] | None:
    """Fetch basic conference data by ID."""
    query = text("""
        SELECT id, name, slug, status, owner_id, location, logo, color, start_date, end_date
        FROM public.conferences
        WHERE id = :conference_id
    """)
    result = await session.execute(query, {"conference_id": conference_id})
    row = result.mappings().one_or_none()
    return dict(row) if row else None


async def list_committees_for_conference(
    session: AsyncSession,
    conference_id: int,
) -> list[dict[str, Any]]:
    """Fetch all committees belonging to a conference."""
    query = text("""
        SELECT id, conference_id, name, code, logo, topic, status, created_at
        FROM public.committees
        WHERE conference_id = :conference_id
        ORDER BY id ASC
    """)
    result = await session.execute(query, {"conference_id": conference_id})
    return [dict(r) for r in result.mappings().all()]


async def get_user_conference_role(
    session: AsyncSession,
    user_id: UUID,
    conference_id: int,
) -> str | None:
    """Return the user's role in the conference ('owner', 'admin', 'chair', etc.) or None if unauthorized."""
    query = text("""
        SELECT 
            CASE 
                WHEN c.owner_id = :user_id THEN 'owner'
                ELSE ca.role::text
            END AS role
        FROM public.conferences c
        LEFT JOIN public.conference_assignments ca 
            ON ca.conference_id = c.id AND ca.user_id = :user_id
        WHERE c.id = :conference_id
          AND (c.owner_id = :user_id OR ca.user_id = :user_id)
        LIMIT 1
    """)
    result = await session.execute(
        query, {"conference_id": conference_id, "user_id": user_id}
    )
    row = result.mappings().one_or_none()
    return row["role"] if row else None


async def create_committee(
    session: AsyncSession,
    conference_id: int,
    payload: schemas.CommitteeCreate,
) -> dict[str, Any]:
    """Create a new committee inside a conference."""
    query = text("""
        INSERT INTO public.committees
            (conference_id, name, code, logo, topic, status)
        VALUES
            (:conference_id, :name, :code, :logo, :topic, :status)
        RETURNING id, conference_id, name, code, logo, topic, status, created_at
    """)

    result = await session.execute(
        query,
        {
            "conference_id": conference_id,
            "name": payload.name,
            "code": payload.code,
            "logo": payload.logo,
            "topic": payload.topic,
            "status": payload.status,
        },
    )
    return dict(result.mappings().one())


async def enroll_member(
    session: AsyncSession,
    conference_id: int,
    payload: schemas.EnrollMember,
) -> dict[str, Any]:
    """Enroll or assign a member to a conference and auto-link user_id if matching email exists."""
    query = text("""
        INSERT INTO public.conference_assignments
            (conference_id, user_id, name, email, institution, role, committee_id, representation_id)
        VALUES (
            :conference_id,
            (SELECT id FROM auth.users WHERE email = :email LIMIT 1),
            :name,
            :email,
            :institution,
            :role::conference_role,
            :committee_id,
            :representation_id
        )
        RETURNING id, conference_id, user_id, name, email, institution, role, committee_id, representation_id, created_at
    """)

    result = await session.execute(
        query,
        {
            "conference_id": conference_id,
            "name": payload.name,
            "email": payload.email,
            "institution": payload.institution,
            "role": payload.role,
            "committee_id": payload.committee_id,
            "representation_id": payload.representation_id,
        },
    )
    return dict(result.mappings().one())


async def list_conference_members(
    session: AsyncSession,
    conference_id: int,
) -> list[dict[str, Any]]:
    """List all members/assignments enrolled in a conference."""
    query = text("""
        SELECT 
            id, conference_id, user_id, name, email, institution, role,
            committee_id, representation_id, created_at
        FROM public.conference_assignments
        WHERE conference_id = :conference_id
        ORDER BY created_at ASC
    """)
    result = await session.execute(query, {"conference_id": conference_id})
    return [dict(r) for r in result.mappings().all()]


async def get_assignment(
    session: AsyncSession,
    user_id: UUID,
    committee_id: int | None = None,
    session_id: int | None = None,
) -> ConferenceAssignment | None:
    """Fetch assignment for a user in a committee or session context."""
    query = text("""
        SELECT
            :user_id AS user_id,
            c.id AS committee_id,
            conf.id AS conference_id,
            CASE 
                WHEN conf.owner_id = :user_id OR ca.role = 'admin' THEN 'chair'
                WHEN ca.role = 'chair' THEN 'chair'
                ELSE 'delegate'
            END AS role,
            ca.representation_id
        FROM public.committees c
        JOIN public.conferences conf ON conf.id = c.conference_id
        LEFT JOIN public.sessions s ON s.committee_id = c.id
        LEFT JOIN public.conference_assignments ca 
            ON ca.conference_id = conf.id 
           AND ca.user_id = :user_id 
           AND (ca.committee_id = c.id OR ca.committee_id IS NULL)
        WHERE (:committee_id IS NOT NULL AND c.id = :committee_id)
           OR (:session_id IS NOT NULL AND s.id = :session_id)
        ORDER BY (ca.committee_id = c.id) DESC, (ca.role = 'admin') DESC
        LIMIT 1
    """)

    result = await session.execute(
        query,
        {
            "committee_id": committee_id,
            "session_id": session_id,
            "user_id": user_id,
        },
    )
    row = result.mappings().one_or_none()
    if row is None:
        return None

    return ConferenceAssignment(
        user_id=row["user_id"],
        conference_id=row["conference_id"],
        committee_id=row["committee_id"],
        role=row["role"],
        representation_id=row["representation_id"],
    )



