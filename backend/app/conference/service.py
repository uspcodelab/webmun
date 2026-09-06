from typing import Literal
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

import app.access.service as access
from app.core.exceptions import BadRequest, ConflictError, NotFoundError

from . import repository
from .enums import CommitteeRole, ConferenceRole
from .models import Committee, CommitteeAssignment, Conference, ConferenceAssignment, Layout, Representation
from .schemas import CommitteeCreate, ConferenceAssignmentCreate, ConferenceCreate, ParticipantAllocationCreate


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

    layouts = await repository.list_available_layouts(
        session=session, conference_id=conference_id
    )
    if data.layout_id not in {layout.id for layout in layouts}:
        raise BadRequest("Layout is not available for this conference")

    committee = await repository.create_committee(
        session=session, conference_id=conference_id, data=data
    )
    if committee is None:
        raise BadRequest("Could not create committee")

    await repository.copy_layout_seats(
        session=session, layout_id=data.layout_id, committee_id=committee.id
    )

    await repository.upsert_committee_session_assignment(
        session=session,
        committee_id=committee.id,
        user_id=user_id,
        role=CommitteeRole.CHAIR,
    )

    await session.commit()
    return committee


async def list_available_layouts(
    session: AsyncSession, *, conference_id: int, user_id: UUID
) -> list[Layout]:
    await access.verify_can_manage_conference(
        session=session, conference_id=conference_id, user_id=user_id
    )
    return await repository.list_available_layouts(
        session=session, conference_id=conference_id
    )


async def create_conference_assignment(
    session: AsyncSession,
    *,
    conference_id: int,
    created_by: UUID,
    data: ConferenceAssignmentCreate,
) -> dict:
    await access.verify_can_manage_conference(
        session=session, conference_id=conference_id, user_id=created_by
    )
    assignee_id = await repository.get_user_id_by_email(session=session, email=data.email)
    if assignee_id is None:
        raise BadRequest("User email was not found")
    if data.committee_id is not None and not await repository.is_committee_in_conference(
        session=session, conference_id=conference_id, committee_id=data.committee_id
    ):
        raise BadRequest("Committee does not belong to this conference")
    await repository.create_conference_assignment(
        session=session,
        conference_id=conference_id,
        user_id=assignee_id,
        role=data.role,
        committee_id=data.committee_id,
    )
    await session.commit()
    return {
        "conference_id": conference_id,
        "email": data.email,
        "role": data.role,
        "committee_id": data.committee_id,
    }


async def list_conference_assignments(
    session: AsyncSession, *, conference_id: int, user_id: UUID
) -> list[dict]:
    await access.verify_can_manage_conference(
        session=session, conference_id=conference_id, user_id=user_id
    )
    return await repository.list_conference_assignments(
        session=session, conference_id=conference_id
    )


async def list_participant_allocations(
    session: AsyncSession, *, conference_id: int, user_id: UUID
) -> list[dict]:
    await access.verify_can_manage_conference(
        session=session, conference_id=conference_id, user_id=user_id
    )
    return await repository.list_participant_allocations(
        session=session, conference_id=conference_id
    )


async def allocate_participant(
    session: AsyncSession,
    *,
    conference_id: int,
    allocated_by: UUID,
    data: ParticipantAllocationCreate,
) -> CommitteeAssignment:
    await access.verify_can_manage_conference(
        session=session, conference_id=conference_id, user_id=allocated_by
    )
    participant_id = await repository.get_user_id_by_email(session=session, email=data.email)
    if participant_id is None:
        raise BadRequest("User email was not found")
    if not await repository.is_conference_participant(
        session=session, conference_id=conference_id, user_id=participant_id
    ):
        raise BadRequest("User is not a participant in this conference")
    if not await repository.is_committee_in_conference(
        session=session, conference_id=conference_id, committee_id=data.committee_id
    ):
        raise BadRequest("Committee does not belong to this conference")
    representations = await repository.list_committee_representations(
        session=session, committee_id=data.committee_id
    )
    if data.representation_id not in {representation.id for representation in representations}:
        raise BadRequest("Representation is not a seat in this committee")
    assignment = await repository.upsert_participant_committee_assignment(
        session=session,
        user_id=participant_id,
        committee_id=data.committee_id,
        representation_id=data.representation_id,
    )
    if assignment is None:
        raise BadRequest("Could not allocate participant")
    await session.commit()
    return assignment


async def list_committee_representations(
    session: AsyncSession, *, committee_id: int, user_id: UUID
) -> list[Representation]:
    await get_committee(session=session, committee_id=committee_id, user_id=user_id)
    return await repository.list_committee_representations(
        session=session, committee_id=committee_id
    )


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
