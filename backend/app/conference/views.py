from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import app.conference.schemas as schemas
import app.conference.service as service
from app.auth.dep import get_current_user
from app.auth.service import AuthUser
from app.core.database import get_db_session

router = APIRouter()


@router.post("/")
async def create_conference(
    payload: schemas.ConferenceCreate,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
):
    """Endpoint to create a new conference"""
    id = await service.create_conference(
        session=db_session, user_id=current_user.user_id, payload=payload
    )
    return {"id": id, "status": "Created"}


@router.get("/")
async def get_user_conferences(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
): ...


@router.get("/{id}")
async def get_conference_info(
    id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
): ...


@router.post("/{id}/committees")
async def create_committee(
    committee: schemas.CommitteeCreate,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
): ...


@router.post("/{conference_id}")
async def enroll_member(
    member: schemas.EnrollMember,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
): ...


#
