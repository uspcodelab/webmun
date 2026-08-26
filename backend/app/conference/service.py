from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

import app.conference.repository as repository
import app.conference.schemas as schemas


async def create_conference(
    session: AsyncSession, user_id: UUID, payload: schemas.ConferenceCreate
) -> int:
    session_id = await repository.create_conference(
        session=session, user_id=user_id, payload=payload
    )

    return session_id


async def get_user_conferences(session: AsyncSession, user_id: UUID): ...


async def get_conference_info(session: AsyncSession, id: int): ...


async def create_committee(session: AsyncSession, payload: schemas.CommitteeCreate): ...
