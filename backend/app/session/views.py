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
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.access.service import AccessDenied
from app.auth.service import verify_jwt_token
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
    current_user=Depends(verify_jwt_token),
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
    session: AsyncSession = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
):
    await websocket.accept()
    try:
        auth_message = await websocket.receive_json()
        auth_user = verify_jwt_token(
            settings=settings, token=auth_message["access_token"]
        )

        assignment = await access.resolve_committee_assignment(
            session=session, user_id=auth_user.user_id, session_id=session_id
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

    except (InvalidTokenError, AccessDenied, service.ActorResolutionError):
        await websocket.close(code=1008)
        return
