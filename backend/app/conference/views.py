from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dep import get_current_user
from app.auth.service import AuthUser
from app.core.database import get_db_session

from . import service
from .schemas import (
    CommitteeCreate,
    CommitteeRead,
    ConferenceCreate,
    ConferenceRead,
)

router = APIRouter()


@router.post(
    "/conferences",
    status_code=status.HTTP_201_CREATED,
)
async def create_conference_endpoint(
    payload: ConferenceCreate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> ConferenceRead:
    conference = await service.create_conference(
        session=session,
        data=payload,
        owner_id=current_user.user_id,
    )
    return ConferenceRead(**conference.__dict__)


@router.get("/conferences")
async def list_conferences_endpoint(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> list[ConferenceRead]:
    conferences = await service.list_conferences(
        session=session,
        user_id=current_user.user_id,
    )
    return [ConferenceRead(**conference.__dict__) for conference in conferences]


@router.get("/conferences/{conference_id}")
async def get_conference_endpoint(
    conference_id: int,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> ConferenceRead:
    conference = await service.get_conference(
        session=session,
        conference_id=conference_id,
        user_id=current_user.user_id,
    )
    return ConferenceRead(**conference.__dict__)


@router.post(
    "/conferences/{conference_id}/committees",
    status_code=status.HTTP_201_CREATED,
)
async def create_committee_endpoint(
    conference_id: int,
    payload: CommitteeCreate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> CommitteeRead:
    committee = await service.create_committee(
        session=session,
        conference_id=conference_id,
        user_id=current_user.user_id,
        data=payload,
    )
    return CommitteeRead(**committee.__dict__)


@router.get("/conferences/{conference_id}/committees")
async def list_committees_endpoint(
    conference_id: int,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> list[CommitteeRead]:
    committees = await service.list_committees(
        session=session,
        conference_id=conference_id,
        user_id=current_user.user_id,
    )
    return [CommitteeRead(**committee.__dict__) for committee in committees]


@router.get("/committees/{committee_id}")
async def get_committee_endpoint(
    committee_id: int,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> CommitteeRead:
    committee = await service.get_committee(
        session=session,
        committee_id=committee_id,
        user_id=current_user.user_id,
    )
    return CommitteeRead(**committee.__dict__)
