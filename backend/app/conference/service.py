from typing import Literal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

import app.access.service as access
from app.core.exceptions import BadRequest, ConflictError, NotFoundError

from . import repository
from .enums import CommitteeRole, ConferenceRole
from .models import Committee, CommitteeAssignment, Conference
from .schemas import CommitteeCreate, ConferenceCreate


async def create_conference(
    session: AsyncSession,
    *,
    data: ConferenceCreate,
    owner_id: UUID,
) -> Conference:
    if data.start_date is not None and data.end_date is not None:
        if data.start_date > data.end_date:
            raise BadRequest("Conference start_date must be before end_date")

    conference = await repository.create_conference(
        session=session, data=data, owner_id=owner_id
    )
    if conference is None:
        raise BadRequest("Could not create conference")

    await repository.create_conference_assignment(
        session=session,
        conference_id=conference.id,
        user_id=owner_id,
        role=ConferenceRole.OWNER,
    )
    await session.commit()

    return conference


async def list_conferences(
    session: AsyncSession,
    *,
    user_id: UUID,
) -> list[Conference]:
    return await repository.list_user_conferences(session=session, user_id=user_id)


async def get_conference(
    session: AsyncSession,
    *,
    conference_id: int,
    user_id: UUID,
) -> Conference:
    conference = await repository.get_user_conference(
        session=session, conference_id=conference_id, user_id=user_id
    )
    if conference is None:
        raise NotFoundError("Conference not found")
    return conference


async def create_committee(
    session: AsyncSession,
    *,
    conference_id: int,
    user_id: UUID,
    data: CommitteeCreate,
) -> Committee:
    await access.verify_can_manage_conference(
        session=session,
        conference_id=conference_id,
        user_id=user_id,
    )

    committee = await repository.create_committee(
        session=session, conference_id=conference_id, data=data
    )
    if committee is None:
        raise BadRequest("Could not create committee")

    await session.commit()
    return committee


async def list_committees(
    session: AsyncSession,
    *,
    conference_id: int,
    user_id: UUID,
) -> list[Committee]:
    await get_conference(session=session, conference_id=conference_id, user_id=user_id)
    return await repository.list_conference_committees(
        session=session, conference_id=conference_id
    )


async def get_committee(
    session: AsyncSession,
    *,
    committee_id: int,
    user_id: UUID,
) -> Committee:
    committee = await repository.get_user_committee(
        session=session, committee_id=committee_id, user_id=user_id
    )
    if committee is None:
        raise NotFoundError("Committee not found")
    return committee


async def promote_conference_assignment_to_committee_assignment(
    session: AsyncSession,
    *,
    conference_id: int,
    committee_id: int,
    user_id: UUID,
    committee_role: Literal[
        CommitteeRole.CHAIR, CommitteeRole.OBSERVER
    ] = CommitteeRole.CHAIR,
) -> CommitteeAssignment:
    # Conference assignments are team/dashboard roles.
    # Committee assignments are the live-session access projection.
    if committee_role not in {CommitteeRole.CHAIR, CommitteeRole.OBSERVER}:
        raise BadRequest("Only chair or observer session access can be promoted")

    await access.verify_conference_assignment_can_grant_session_access(
        session=session,
        conference_id=conference_id,
        committee_id=committee_id,
        user_id=user_id,
    )

    existing = await repository.get_committee_assignment(
        session=session, committee_id=committee_id, user_id=user_id
    )
    if existing is not None and existing.role == CommitteeRole.DELEGATE:
        raise ConflictError("Cannot replace a delegate committee assignment")

    assignment = await repository.upsert_committee_session_assignment(
        session=session,
        committee_id=committee_id,
        user_id=user_id,
        role=committee_role,
    )
    if assignment is None:
        raise ConflictError("Could not promote committee session access")

    await session.commit()
    return assignment
