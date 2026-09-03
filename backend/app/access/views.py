from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dep import get_current_user
from app.auth.service import AuthUser
from app.core.database import get_db_session

from .schemas import ConferenceAccess, SessionRepresentation
from .service import get_my_conference_access, resolve_session_assignment

router = APIRouter()


@router.get("/sessions/{session_id}/me")
async def get_my_session_access(
    session_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> SessionRepresentation:
    """Return the authenticated user's actor context for a session."""
    assignment = await resolve_session_assignment(
        db_session, current_user.user_id, session_id
    )

    return SessionRepresentation(
        role=assignment.role, representation_id=assignment.representation_id
    )


@router.get("/conferences/{conference_id}/me")
async def get_my_conference_access_endpoint(
    conference_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
) -> ConferenceAccess:
    """Return the authenticated user's dashboard/team access for a conference."""
    return await get_my_conference_access(
        db_session, current_user.user_id, conference_id
    )
