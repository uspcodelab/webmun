from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import app.conference.schemas as schemas
import app.conference.service as service
import app.session.schemas as session_schemas
from app.auth.dep import get_current_user
from app.auth.service import AuthUser
from app.conference.models import ConferenceAssignment
from app.core.database import get_db_session

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_conference(
    payload: schemas.ConferenceCreate,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> dict[str, Any]:
    """Endpoint to create a new conference"""
    conference_id = await service.create_conference(
        session=db_session, user_id=current_user.user_id, payload=payload
    )
    return {"id": conference_id, "status": "Created"}


@router.get("/")
async def get_user_conferences(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> list[schemas.ConferenceSummary]:
    """Return dashboard summaries for the authenticated user's conferences."""
    return await service.get_user_conferences(
        session=db_session, user_id=current_user.user_id
    )


@router.get("/{id}")
async def get_conference_info(
    id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> schemas.ConferenceDetail:
    """Endpoint to get detailed conference information and committees"""
    return await service.get_conference_info(
        session=db_session, user_id=current_user.user_id, conference_id=id
    )


@router.post(
    "/{id}/committees",
    status_code=status.HTTP_201_CREATED,
)
async def create_committee(
    id: int,
    committee: schemas.CommitteeCreate,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> schemas.CommitteeResponse:
    """Endpoint to create a new committee in a conference"""
    return await service.create_committee(
        session=db_session,
        user_id=current_user.user_id,
        conference_id=id,
        payload=committee,
    )


@router.post(
    "/{conference_id}/members",
    status_code=status.HTTP_201_CREATED,
)
async def enroll_member(
    conference_id: int,
    member: schemas.EnrollMember,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> ConferenceAssignment:
    """Endpoint to enroll/assign a member to a conference"""
    return await service.enroll_member(
        session=db_session,
        user_id=current_user.user_id,
        conference_id=conference_id,
        payload=member,
    )


@router.get("/{conference_id}/members")
async def list_conference_members(
    conference_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> list[ConferenceAssignment]:
    """Endpoint to list all members assigned to a conference"""
    return await service.list_conference_members(
        session=db_session,
        user_id=current_user.user_id,
        conference_id=conference_id,
    )


@router.get("/sessions/{session_id}/me")
async def get_my_session_access(
    session_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> session_schemas.SessionRepresentation:
    """Return the authenticated user's assignment context for a session."""
    assignment = await service.resolve_session_assignment(
        session=db_session, user_id=current_user.user_id, session_id=session_id
    )
    return session_schemas.SessionRepresentation(
        role=assignment.role,
        representation_id=assignment.representation_id,
    )
