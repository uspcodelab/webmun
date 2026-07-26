from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dep import get_current_user
from app.auth.service import AuthUser
from app.core.database import get_db_session

from .service import AccessDenied, resolve_session_assignment

router = APIRouter()


@router.get("/sessions/{session_id}/me")
async def get_my_session_access(
    session_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
):
    """Return the authenticated user's actor context for a session."""
    try:
        assignment = await resolve_session_assignment(
            db_session, current_user.user_id, session_id
        )
    except AccessDenied as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )

    return {
        "role": assignment.role,
        "representation_id": assignment.representation_id,
    }
