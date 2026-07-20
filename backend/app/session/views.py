# An adapter. Accepts HTTP/Websockets messages, validates envelopes, calls/attaches services and return/send errors
# The 1st layer when connecting to clients

from fastapi import (
    APIRouter,
    Depends,
    Response,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.access.service import AccessDenied
from app.auth.dep import get_current_user
from app.auth.service import verify_jwt_token, TokenInvalidError, TokenExpiredError
from app.core.config import Settings
from app.core.dep import get_connection_manager, get_logger, get_session_engine
from app.core.config import get_settings
from app.core.database import get_db_session
from app.session.enums import ChairEvents, DelegateEvents, SessionRole
from app.session.models import SessionLiveState
from app.session.schemas import SessionCreationSchema, SessionEvent

import app.access.service as access
import app.session.service as service

router = APIRouter()


# Workaround to make FastApi add all the Schemas to the OpenApi file
@router.get("/dummy", status_code=status.HTTP_404_NOT_FOUND)
async def dummy(
    name: SessionEvent,
    schemas: SessionLiveState,
    enum1: DelegateEvents,
    enum2: ChairEvents,
):
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return Response(status_code=status.HTTP_200_OK)


# Create committee route, receives a contentbody following CommitteeCreationSchema's format
@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_session_endpoint(
    session_schema: SessionCreationSchema,
    session: AsyncSession = Depends(get_db_session),
    manager=Depends(get_connection_manager),
    current_user=Depends(get_current_user), # TODO: map out that only admins can create sessions
):
    # Mock a session being created
    await service.create_session_service(
        manager=manager,
        session=session,
        session_schema=session_schema,
        creator_uuid=current_user.id,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: int,
    manager=Depends(get_connection_manager),
    engine=Depends(get_session_engine),
    logger=Depends(get_logger),
    settings: Settings = Depends(get_settings),
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
                session=db, user_id=auth_user.user_id, session_id=session_id
            )

        actor = service.build_actor(
            manager=manager,
            session_id=session_id,
            role=SessionRole(assignment.role),
            delegation_id=assignment.delegation_id,
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

