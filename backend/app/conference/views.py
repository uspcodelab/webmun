from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import app.conference.schemas as schemas
import app.conference.service as service
from app.auth.dep import get_current_user
from app.auth.service import AuthUser
from app.core.database import get_db_session

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_conference(
    payload: schemas.ConferenceCreate,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
):
    """Endpoint to create a new conference"""
    conference_id = await service.create_conference(
        session=db_session, user_id=current_user.user_id, payload=payload
    )
    return {"id": conference_id, "status": "Created"}


@router.get("/", response_model=list[int])
async def get_user_conferences(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
):
    """Endpoint to get list of conference ids for a user"""
    return await service.get_user_conferences(
        session=db_session, user_id=current_user.user_id
    )


@router.get("/{id}", response_model=schemas.ConferenceDetail)
async def get_conference_info(
    id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
):
    """Endpoint to get detailed conference information and committees"""
    return await service.get_conference_info(
        session=db_session, user_id=current_user.user_id, conference_id=id
    )


@router.post(
    "/{id}/committees",
    response_model=schemas.CommitteeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_committee(
    id: int,
    committee: schemas.CommitteeCreate,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
):
    """Endpoint to create a new committee in a conference"""
    return await service.create_committee(
        session=db_session,
        user_id=current_user.user_id,
        conference_id=id,
        payload=committee,
    )


@router.post(
    "/{conference_id}/members",
    response_model=schemas.AssignmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def enroll_member(
    conference_id: int,
    member: schemas.EnrollMember,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
):
    """Endpoint to enroll/assign a member to a conference"""
    return await service.enroll_member(
        session=db_session,
        user_id=current_user.user_id,
        conference_id=conference_id,
        payload=member,
    )


@router.get(
    "/{conference_id}/members",
    response_model=list[schemas.AssignmentResponse],
)
async def list_conference_members(
    conference_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
):
    """Endpoint to list all members assigned to a conference"""
    return await service.list_conference_members(
        session=db_session,
        user_id=current_user.user_id,
        conference_id=conference_id,
    )
