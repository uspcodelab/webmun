# An adapter. Accepts HTTP/Websockets messages, validates envelopes, calls/attaches services and return/send errors
# The 1st layer when connecting to clients

from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Response,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.access.service import AccessDenied
from app.auth.dep import get_current_user
from app.auth.service import AuthUser, verify_jwt_token, TokenInvalidError, TokenExpiredError
from app.core.config import Settings
from app.core.dep import get_connection_manager, get_logger, get_session_engine
from app.core.config import get_settings
from app.core.database import get_db_session
from app.session.engine import SessionEngine
from app.session.enums import ChairEvents, DelegateEvents, SessionRole
from app.session.manager import ConnectionManager
from app.session.models import SessionLiveState
from app.session.schemas import SessionCreationSchema, SessionEvent

import app.access.service as access
import app.session.repository as repository
import app.session.service as service
import logging

router = APIRouter()


# Workaround to make FastApi add all the Schemas to the OpenApi file
@router.get("/dummy", status_code=status.HTTP_404_NOT_FOUND)
async def dummy(
    name: SessionEvent,
    schemas: SessionLiveState,
    enum1: DelegateEvents,
    enum2: ChairEvents,
):
    """Dummy workaround to make FastAPI add all schemas to the OpenAPI file"""
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/health", status_code=status.HTTP_200_OK)
async def health():
    """Healthcheck route"""
    return Response(status_code=status.HTTP_200_OK)


@router.post("/", status_code=status.HTTP_200_OK)
async def create_session_endpoint(
    session_schema: SessionCreationSchema,
    session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[AuthUser, Depends(get_current_user)], # TODO: map out that only admins can create sessions
):
    """POST endpoint to create a new session"""
    try:
        await access.verify_user_role(
            session=session,
            user_id=current_user.user_id,
            committee_id=session_schema.committee_id,
            required_role="chair",
        )

        res = await service.create_session_service(
            session=session,
            session_schema=session_schema,
        )
        return {"id": res, "status": "Created"}

    except AccessDenied as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )
    except service.SessionCreationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) 


@router.post("/{session_id}/activate", status_code=status.HTTP_204_NO_CONTENT)
async def activate_session_endpoint(
    session_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
    current_user: Annotated[AuthUser, Depends(get_current_user)],
):
    """Endpoint to activate a planned session"""
    try:
        stored = await repository.get_session_info(
            session=db_session,
            committee_session_id=session_id,
        )
        if stored is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

        await access.verify_user_role(
            session=db_session,
            user_id=current_user.user_id,
            committee_id=stored.committee_id,
            required_role="chair",
        )

        await service.activate_session(
            session=db_session, 
            manager=manager,
            committee_session_id=session_id)
    except AccessDenied as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        )
    except service.SessionFetchError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except service.SessionUpdateError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc)
        )



@router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: int,
    committee_id: int,
    manager: Annotated[ConnectionManager, Depends(get_connection_manager)],
    engine: Annotated[SessionEngine, Depends(get_session_engine)],
    logger: Annotated[logging.Logger, Depends(get_logger)],
    settings: Annotated[Settings, Depends(get_settings)],
):
    """
    Endpoint for connecting to a committee session.

    Overall flow: accepts websocket -> user sends token -> we verify it ->
    if valid, lookup an assigment -> builds actor, connects to manager, and receive The
    current session state
    """

    await websocket.accept()
    try:
        auth_message = await websocket.receive_json()
        # we use pure verify_jwt_token due to websocket not handling bearer-header support
        auth_user = verify_jwt_token(
            settings=settings, token=auth_message["access_token"]
        )
        
        # short db scope for access lookup at first connection
        session_factory = websocket.app.state.db_session_factory
        async with session_factory() as db: 
            assignment = await access.resolve_committee_assignment(
                session=db, user_id=auth_user.user_id, committee_id=committee_id
            )

        actor = service.build_actor(
            manager=manager,
            session_id=session_id,
            role=SessionRole(assignment.role.upper()),
            delegation_id=assignment.representation_id,
        )

        await manager.connect(websocket, session_id, actor)
        try:
            while True:
                data = await websocket.receive_text()
                await service.handle_client_messages(
                    manager=manager,
                    engine=engine,
                    logger=logger,
                    session_id=session_id,
                    actor=actor,
                    data=data,
                )

        except WebSocketDisconnect:
            manager.disconnect(websocket, session_id)

    except (TokenExpiredError, TokenInvalidError, AccessDenied, service.ActorResolutionError) as exc:
        if isinstance(exc, TokenExpiredError):
            reason = "token_expired"
        elif isinstance(exc, TokenInvalidError):
            reason = "token_invalid"
        elif isinstance(exc, AccessDenied):
            reason = "access_denied"
        else:
            reason = "actor_resolution_error"

        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason=reason)
        return
